from fastapi import APIRouter
from .documents import router as documents_router
from .jobs import router as jobs_router
from .models import router as models_router
from .eval import router as eval_router
from .health import router as health_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(health_router)
api_router.include_router(documents_router)
api_router.include_router(jobs_router)
api_router.include_router(models_router)
api_router.include_router(eval_router)

__all__ = ["api_router"]
