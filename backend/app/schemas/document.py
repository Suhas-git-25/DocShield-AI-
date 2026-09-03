"""
DocShield AI - Pydantic Schemas
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

class FieldResult(BaseModel):
    field_name: str
    value: str
    confidence: float
    anomaly_flag: bool = False
    anomaly_reason: Optional[str] = None
    bbox: Optional[List[float]] = None  # [x1, y1, x2, y2] normalized (0-1)

class ForgerySignal(BaseModel):
    attack_type_guess: Optional[str] = None
    confidence: float
    anomaly_score: float = 0.0
    region_bbox: Optional[List[float]] = None  # [x1, y1, x2, y2] normalized
    description: Optional[str] = None

class RuleCheckResult(BaseModel):
    check_name: str
    passed: bool
    severity: Literal["low", "medium", "high"] = "low"
    details: str

class AnalyzeResponse(BaseModel):
    doc_id: str
    document_type: str
    risk_score: float  # 0.0 to 1.0
    risk_level: Literal["low", "medium", "high"]
    is_authentic: bool
    summary_reason: str
    fields: List[FieldResult]
    forgery_signals: List[ForgerySignal]
    rule_checks: List[RuleCheckResult] = []
    heatmap_url: Optional[str] = None
    original_image_url: Optional[str] = None
    model_versions: Dict[str, str] = Field(default_factory=dict)
    processing_time_ms: int

class JobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "completed", "failed"]
    created_at: str
    result: Optional[AnalyzeResponse] = None
    error: Optional[str] = None

class ModelVersionInfo(BaseModel):
    stage: str
    active_version: str
    available_versions: List[str]
    description: str
    metrics: Dict[str, Any] = Field(default_factory=dict)

class ModelActivateRequest(BaseModel):
    version: str

class RobustnessMetrics(BaseModel):
    accuracy: float
    f1_score: float
    auroc: float
    auprc: float
    localization_iou: float
    generalization_gap: float
    per_attack_recall: Dict[str, float]
    tier_accuracy: Dict[str, float]

class RobustnessReport(BaseModel):
    report_id: str
    generated_at: str
    model_version_a: str
    model_version_b: str
    metrics_a: RobustnessMetrics
    metrics_b: RobustnessMetrics
    improvement_summary: Dict[str, float]
    recommendations: List[str]

class AttackTestRequest(BaseModel):
    doc_id: Optional[str] = None
    attack_type: str
    severity: Literal["easy", "medium", "hard"] = "medium"

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    models_loaded: Dict[str, bool]
    storage_accessible: bool
