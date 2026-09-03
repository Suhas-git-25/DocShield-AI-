"""
DocShield AI - Health Check API
"""

import time
import os
from fastapi import APIRouter
from ..schemas.document import HealthResponse
from ..services.model_registry import model_registry
from ..config import settings

router = APIRouter(tags=["health"])

START_TIME = time.time()

@router.get("/health", response_model=HealthResponse)
def get_health():
    """Liveness / Readiness probe."""
    active_models = model_registry.get_active_versions_dict()
    storage_ok = os.path.exists(settings.UPLOAD_DIR) and os.path.exists(settings.HEATMAP_DIR)

    return HealthResponse(
        status="healthy",
        version=settings.VERSION,
        uptime_seconds=round(time.time() - START_TIME, 2),
        models_loaded={stage: True for stage in active_models.keys()},
        storage_accessible=storage_ok
    )
