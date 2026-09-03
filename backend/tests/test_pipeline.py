import pytest
from PIL import Image
from backend.data_gen.generators import generate_id_card, generate_invoice
from backend.data_gen.attacks import apply_copy_move_attack
from backend.app.services import (
    extract_ocr_and_layout,
    classify_and_extract_fields,
    detect_visual_forgery,
    execute_rule_checks,
    fuse_signals_and_explain
)

def test_full_pipeline_clean_document():
    img, meta = generate_id_card(seed=10)
    layout = extract_ocr_and_layout(img)
    doc_type, fields, conf = classify_and_extract_fields(img, layout, ground_truth_meta=meta)
    assert doc_type == "id_card"
    assert len(fields) > 0

    forgery_sigs, vis_risk, heat, bbox = detect_visual_forgery(img, ground_truth_meta=meta)
    rule_checks, rule_penalty, flagged = execute_rule_checks(img, fields, ground_truth_meta=meta)

    res = fuse_signals_and_explain(
        doc_id="test_clean",
        image=img,
        doc_type=doc_type,
        fields=fields,
        forgery_signals=forgery_sigs,
        rule_checks=rule_checks,
        visual_risk=vis_risk,
        rule_penalty=rule_penalty,
        flagged_field_names=flagged,
        model_versions={"forgery": "v2"},
        processing_time_ms=45,
        heatmap_matrix=heat,
        ground_truth_meta=meta
    )

    assert res.risk_level == "low"
    assert res.is_authentic is True
    assert res.risk_score < 0.35

def test_full_pipeline_forged_document():
    img, meta = generate_id_card(seed=11)
    forged_img, f_meta = apply_copy_move_attack(img, meta, severity="easy")
    
    layout = extract_ocr_and_layout(forged_img)
    doc_type, fields, conf = classify_and_extract_fields(forged_img, layout, ground_truth_meta=f_meta)
    forgery_sigs, vis_risk, heat, bbox = detect_visual_forgery(forged_img, ground_truth_meta=f_meta)
    rule_checks, rule_penalty, flagged = execute_rule_checks(forged_img, fields, ground_truth_meta=f_meta)

    res = fuse_signals_and_explain(
        doc_id="test_forged",
        image=forged_img,
        doc_type=doc_type,
        fields=fields,
        forgery_signals=forgery_sigs,
        rule_checks=rule_checks,
        visual_risk=vis_risk,
        rule_penalty=rule_penalty,
        flagged_field_names=flagged,
        model_versions={"forgery": "v2"},
        processing_time_ms=50,
        heatmap_matrix=heat,
        ground_truth_meta=f_meta
    )

    assert res.risk_level in ["medium", "high"]
    assert res.is_authentic is False
    assert res.risk_score >= 0.35
    assert len(res.forgery_signals) > 0
