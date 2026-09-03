"""
DocShield AI - Multi-Signal Risk Fusion Engine
Combines visual model scores, ELA features, and rule check outcomes into a calibrated risk score,
risk classification, field-level anomaly flags, and human-readable explanations.
"""

import os
import numpy as np
from PIL import Image
from typing import List, Dict, Any, Tuple, Optional

from ..schemas.document import AnalyzeResponse, FieldResult, ForgerySignal, RuleCheckResult
from ..utils.image_processing import overlay_heatmap_on_image
from ..config import settings

def fuse_signals_and_explain(
    doc_id: str,
    image: Image.Image,
    doc_type: str,
    fields: List[FieldResult],
    forgery_signals: List[ForgerySignal],
    rule_checks: List[RuleCheckResult],
    visual_risk: float,
    rule_penalty: float,
    flagged_field_names: List[str],
    model_versions: Dict[str, str],
    processing_time_ms: int,
    heatmap_matrix: np.ndarray,
    ground_truth_meta: Optional[Dict[str, Any]] = None
) -> AnalyzeResponse:
    """
    Fuses all forensic signals and produces an AnalyzeResponse payload.
    """
    # Calculate fused risk score
    # Weights: 50% visual forgery, 50% rule/metadata violations
    fused_score = (visual_risk * 0.55) + (rule_penalty * 0.45)
    fused_score = float(np.clip(fused_score, 0.04, 0.98))
    fused_score = round(fused_score, 3)

    # Determine risk level
    if fused_score < settings.RISK_THRESHOLD_LOW:
        risk_level = "low"
        is_authentic = True
    elif fused_score < settings.RISK_THRESHOLD_HIGH:
        risk_level = "medium"
        is_authentic = False
    else:
        risk_level = "high"
        is_authentic = False

    # Update field anomaly flags
    updated_fields = []
    for f in fields:
        is_anomaly = f.field_name in flagged_field_names
        anomaly_reason = None
        if is_anomaly:
            anomaly_reason = f"Flagged by forensics engine: Inconsistent typography, modified values, or math discrepancy on '{f.field_name}'."
        
        updated_fields.append(FieldResult(
            field_name=f.field_name,
            value=f.value,
            confidence=f.confidence,
            anomaly_flag=is_anomaly,
            anomaly_reason=anomaly_reason,
            bbox=f.bbox
        ))

    # Compose executive summary explanation
    reasons = []
    if forgery_signals:
        for s in forgery_signals:
            if s.description:
                reasons.append(s.description)
    
    for r in rule_checks:
        if not r.passed:
            reasons.append(r.details)

    if not reasons:
        summary_reason = "Document passed all visual, structural, and metadata verification checks with high integrity."
    else:
        summary_reason = " | ".join(reasons)

    # Save heatmap overlay to storage
    heatmap_filename = f"{doc_id}_heatmap.png"
    heatmap_path = os.path.join(settings.HEATMAP_DIR, heatmap_filename)
    overlay_img = overlay_heatmap_on_image(image, heatmap_matrix, alpha=0.52, colormap="turbo")
    overlay_img.save(heatmap_path, format="PNG")

    # Also save original image for side-by-side display
    orig_filename = f"{doc_id}_original.png"
    orig_path = os.path.join(settings.UPLOAD_DIR, orig_filename)
    image.save(orig_path, format="PNG")

    heatmap_url = f"/v1/documents/{doc_id}/heatmap"
    orig_url = f"/v1/documents/{doc_id}/original"

    return AnalyzeResponse(
        doc_id=doc_id,
        document_type=doc_type,
        risk_score=fused_score,
        risk_level=risk_level,
        is_authentic=is_authentic,
        summary_reason=summary_reason,
        fields=updated_fields,
        forgery_signals=forgery_signals,
        rule_checks=rule_checks,
        heatmap_url=heatmap_url,
        original_image_url=orig_url,
        model_versions=model_versions,
        processing_time_ms=processing_time_ms
    )
