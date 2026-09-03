"""
DocShield AI - Models API
Lists model stages, active versions, and handles dynamic model stage switching.
"""

from typing import List
from fastapi import APIRouter, HTTPException
from ..schemas.document import ModelVersionInfo, ModelActivateRequest
from ..services.model_registry import model_registry

router = APIRouter(prefix="/models", tags=["models"])

@router.get("", response_model=List[ModelVersionInfo])
def list_models():
    """Returns available model stages and active versions."""
    return model_registry.get_all_models()

@router.post("/{stage}/activate")
def activate_model_version(stage: str, req: ModelActivateRequest):
    """Activates a specific model version for a given pipeline stage."""
    success = model_registry.activate_version(stage, req.version)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid stage '{stage}' or version '{req.version}' is not registered."
        )
    return {
        "status": "success",
        "stage": stage,
        "active_version": req.version,
        "message": f"Successfully switched {stage} active version to {req.version}"
    }
