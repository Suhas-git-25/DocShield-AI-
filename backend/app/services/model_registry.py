"""
DocShield AI - Model Registry Service
Manages versioning and runtime activation across pipeline stages (OCR, Understanding, Forgery ViT, Risk Fusion).
"""

from typing import Dict, List, Any
from ..schemas.document import ModelVersionInfo

class ModelRegistry:
    def __init__(self):
        self._registry = {
            "ocr": {
                "active": "v1.2.0-trocr-printed",
                "available": ["v1.0.0-tesseract-base", "v1.2.0-trocr-printed", "v2.0.0-donut-finetuned"],
                "description": "Optical Character Recognition and bounding box layout extractor.",
                "metrics": {"cer": 0.021, "wer": 0.048, "latency_ms": 120}
            },
            "understanding": {
                "active": "v2.1.0-layoutlmv3-finetuned",
                "available": ["v1.0.0-layoutlmv2-base", "v2.0.0-layoutlmv3-base", "v2.1.0-layoutlmv3-finetuned"],
                "description": "Multi-modal Document Entity Extraction and Type Classification.",
                "metrics": {"f1_macro": 0.942, "accuracy": 0.961, "latency_ms": 85}
            },
            "forgery": {
                "active": "v2.0.0-vit-adversarial-phase2",
                "available": ["v1.0.0-vit-baseline-phase1", "v2.0.0-vit-adversarial-phase2", "v2.1.0-convnext-robust"],
                "description": "Visual Tampering, ELA Disparity & Patch Correlation Classifier.",
                "metrics": {"auroc": 0.968, "f1_score": 0.935, "heldout_recall": 0.892}
            },
            "fusion": {
                "active": "v1.1.0-calibrated-rules",
                "available": ["v1.0.0-simple-average", "v1.1.0-calibrated-rules"],
                "description": "Bayesian Multi-Signal Calibrated Risk Fusion Engine.",
                "metrics": {"brier_score": 0.041, "ece": 0.028}
            }
        }

    def get_all_models(self) -> List[ModelVersionInfo]:
        results = []
        for stage, data in self._registry.items():
            results.append(ModelVersionInfo(
                stage=stage,
                active_version=data["active"],
                available_versions=data["available"],
                description=data["description"],
                metrics=data["metrics"]
            ))
        return results

    def get_active_versions_dict(self) -> Dict[str, str]:
        return {stage: data["active"] for stage, data in self._registry.items()}

    def activate_version(self, stage: str, version: str) -> bool:
        if stage not in self._registry:
            return False
        if version not in self._registry[stage]["available"]:
            return False
        self._registry[stage]["active"] = version
        return True

model_registry = ModelRegistry()
