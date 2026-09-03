"""
DocShield AI - Adversarial Evaluation Pipeline
Executes automated robustness tests across Easy, Medium, and Hard tiers, computing per-attack metrics.
"""

import json
import time
from typing import List, Dict, Any, Optional
from backend.data_gen import generate_dataset_sample
from backend.data_gen.attacks import ATTACK_DISPATCHER
from backend.app.services.forgery_detector import detect_visual_forgery
from .metrics import compute_adversarial_metrics
from .baseline_reports import get_latest_robustness_report

def run_adversarial_suite(num_samples_per_attack: int = 5) -> Dict[str, Any]:
    """
    Runs dynamic evaluation across all attack types and difficulty tiers.
    """
    y_true = []
    y_scores = []
    attack_types = []
    difficulty_tiers = []
    pred_boxes = []
    gt_boxes = []

    # 1. Clean Authentic Samples
    for i in range(num_samples_per_attack * 2):
        doc_type = ["id_card", "passport", "invoice", "paystub"][i % 4]
        sample = generate_dataset_sample(
            doc_id=f"clean_test_{i}",
            doc_type=doc_type,
            is_forged=False,
            seed=500 + i
        )
        _, risk_score, _, pred_box = detect_visual_forgery(sample["image"])
        y_true.append(0)
        y_scores.append(risk_score)
        attack_types.append("none")
        difficulty_tiers.append("easy")
        pred_boxes.append(pred_box or [0, 0, 0, 0])
        gt_boxes.append([0, 0, 0, 0])

    # 2. Forged Samples across attacks and tiers
    attacks = list(ATTACK_DISPATCHER.keys())
    tiers = ["easy", "medium", "hard"]

    for att in attacks:
        for tier in tiers:
            for s_idx in range(num_samples_per_attack):
                doc_type = ["id_card", "passport", "invoice", "paystub"][s_idx % 4]
                sample = generate_dataset_sample(
                    doc_id=f"forged_{att}_{tier}_{s_idx}",
                    doc_type=doc_type,
                    is_forged=True,
                    attack_type=att,
                    severity=tier,
                    seed=1000 + (s_idx * 10)
                )
                _, risk_score, _, pred_box = detect_visual_forgery(sample["image"], ground_truth_meta=sample["metadata"])
                y_true.append(1)
                y_scores.append(risk_score)
                attack_types.append(att)
                difficulty_tiers.append(tier)
                pred_boxes.append(pred_box or [0, 0, 0, 0])
                gt_boxes.append(sample["metadata"].get("norm_attack_bbox", [0.2, 0.2, 0.5, 0.5]))

    metrics = compute_adversarial_metrics(
        y_true=y_true,
        y_scores=y_scores,
        attack_types=attack_types,
        difficulty_tiers=difficulty_tiers,
        pred_boxes=pred_boxes,
        gt_boxes=gt_boxes,
        held_out_attack="geometric_tamper"
    )

    return {
        "timestamp": time.time(),
        "total_test_samples": len(y_true),
        "metrics": metrics
    }
