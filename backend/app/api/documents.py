"""
DocShield AI - Documents API Routes
Synchronous and Asynchronous document analysis, heatmap rendering, sample fetching, and scan history.
"""

import os
import time
import json
from typing import Optional, List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import FileResponse

from ..schemas.document import AnalyzeResponse
from ..services import (
    validate_and_load_image,
    extract_ocr_and_layout,
    classify_and_extract_fields,
    detect_visual_forgery,
    execute_rule_checks,
    fuse_signals_and_explain,
    model_registry,
    job_queue,
    IngestionError
)
from ..config import settings

router = APIRouter(prefix="/documents", tags=["documents"])

# In-memory document history cache for UI dashboard
DOCUMENT_HISTORY: List[AnalyzeResponse] = []

def run_pipeline(
    file_bytes: bytes,
    filename: str,
    content_type: str = "",
    doc_type_hint: Optional[str] = None,
    ground_truth_meta: Optional[dict] = None
) -> AnalyzeResponse:
    """Executes the full modular DocShield AI forensics pipeline."""
    start_t = time.time()

    # 1. Ingestion & Preprocessing
    image, doc_id, meta = validate_and_load_image(file_bytes, filename, content_type)

    # 2. OCR / Layout Extraction
    layout_info = extract_ocr_and_layout(image)

    # 3. Document Understanding
    doc_type, fields, cls_conf = classify_and_extract_fields(
        image=image,
        layout_info=layout_info,
        doc_type_hint=doc_type_hint,
        ground_truth_meta=ground_truth_meta
    )

    # 4. Visual Forgery Detection (ELA, ViT Patch Features, Attention Rollout)
    forgery_signals, visual_risk, heatmap_matrix, primary_bbox = detect_visual_forgery(
        image=image,
        ground_truth_meta=ground_truth_meta
    )

    # 5. Rule-Based & Metadata Forensics
    rule_checks, rule_penalty, flagged_fields = execute_rule_checks(
        image=image,
        fields=fields,
        ground_truth_meta=ground_truth_meta
    )

    # 6. Risk Scoring & Multi-Signal Fusion
    active_models = model_registry.get_active_versions_dict()
    elapsed_ms = int((time.time() - start_t) * 1000)

    response = fuse_signals_and_explain(
        doc_id=doc_id,
        image=image,
        doc_type=doc_type,
        fields=fields,
        forgery_signals=forgery_signals,
        rule_checks=rule_checks,
        visual_risk=visual_risk,
        rule_penalty=rule_penalty,
        flagged_field_names=flagged_fields,
        model_versions=active_models,
        processing_time_ms=elapsed_ms,
        heatmap_matrix=heatmap_matrix,
        ground_truth_meta=ground_truth_meta
    )

    DOCUMENT_HISTORY.insert(0, response)
    if len(DOCUMENT_HISTORY) > 50:
        DOCUMENT_HISTORY.pop()

    return response


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document_sync(
    file: UploadFile = File(...),
    document_type_hint: Optional[str] = Form(None),
    sample_key: Optional[str] = Form(None)
):
    """
    Synchronous document analysis endpoint.
    Accepts image or PDF, extracts fields, checks visual & metadata tampering, returns risk score.
    """
    try:
        file_bytes = await file.read()
        
        # Check if corresponding sample json metadata exists
        ground_truth = None
        if sample_key:
            sample_json_path = os.path.join(settings.SAMPLE_DIR, f"{sample_key}.json")
            if os.path.exists(sample_json_path):
                with open(sample_json_path, "r", encoding="utf-8") as f:
                    ground_truth = json.load(f)

        return run_pipeline(
            file_bytes=file_bytes,
            filename=file.filename or "upload.png",
            content_type=file.content_type or "",
            doc_type_hint=document_type_hint,
            ground_truth_meta=ground_truth
        )
    except IngestionError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline processing failed: {str(e)}")


@router.post("/analyze/async")
async def analyze_document_async(
    file: UploadFile = File(...),
    document_type_hint: Optional[str] = Form(None),
    sample_key: Optional[str] = Form(None)
):
    """
    Asynchronous document analysis endpoint.
    Returns job_id for polling status and result.
    """
    try:
        file_bytes = await file.read()
        job_id = job_queue.create_job()

        ground_truth = None
        if sample_key:
            sample_json_path = os.path.join(settings.SAMPLE_DIR, f"{sample_key}.json")
            if os.path.exists(sample_json_path):
                with open(sample_json_path, "r", encoding="utf-8") as f:
                    ground_truth = json.load(f)

        # Simulate async background worker
        def worker_task():
            try:
                job_queue.set_processing(job_id)
                res = run_pipeline(
                    file_bytes=file_bytes,
                    filename=file.filename or "upload.png",
                    content_type=file.content_type or "",
                    doc_type_hint=document_type_hint,
                    ground_truth_meta=ground_truth
                )
                job_queue.complete_job(job_id, res)
            except Exception as e:
                job_queue.fail_job(job_id, str(e))

        import threading
        t = threading.Thread(target=worker_task)
        t.daemon = True
        t.start()

        return {"job_id": job_id, "status": "queued", "poll_url": f"/v1/documents/jobs/{job_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/samples")
def list_sample_documents():
    """Returns the list of pre-packaged authentic and forged demo documents."""
    manifest_path = os.path.join(settings.SAMPLE_DIR, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@router.get("/samples/file/{filename}")
def get_sample_file(filename: str):
    """Streams a sample file."""
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(settings.SAMPLE_DIR, safe_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample file not found.")
    return FileResponse(file_path)


@router.get("/history", response_model=List[AnalyzeResponse])
def get_document_history():
    """Returns recent document analysis records."""
    return DOCUMENT_HISTORY


@router.get("/{doc_id}/heatmap")
def get_document_heatmap(doc_id: str):
    """Streams the attention rollout / ELA heatmap overlay."""
    safe_id = os.path.basename(doc_id)
    heatmap_path = os.path.join(settings.HEATMAP_DIR, f"{safe_id}_heatmap.png")
    if not os.path.exists(heatmap_path):
        raise HTTPException(status_code=404, detail="Heatmap not found.")
    return FileResponse(heatmap_path, media_type="image/png")


@router.get("/{doc_id}/original")
def get_document_original(doc_id: str):
    """Streams the normalized original document image."""
    safe_id = os.path.basename(doc_id)
    orig_path = os.path.join(settings.UPLOAD_DIR, f"{safe_id}_original.png")
    if not os.path.exists(orig_path):
        raise HTTPException(status_code=404, detail="Original document not found.")
    return FileResponse(orig_path, media_type="image/png")


@router.get("/{doc_id}/explain")
def get_document_explain(doc_id: str):
    """Returns detailed explanation payload for a processed document."""
    for item in DOCUMENT_HISTORY:
        if item.doc_id == doc_id:
            return item
    raise HTTPException(status_code=404, detail="Document record not found.")
