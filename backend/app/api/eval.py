"""
DocShield AI - Evaluation & Robustness API
Returns adversarial robustness benchmark reports and executes dynamic attack sandbox tests.
"""

from fastapi import APIRouter, HTTPException
from ..schemas.document import RobustnessReport, AttackTestRequest
from backend.eval.baseline_reports import get_latest_robustness_report
from backend.eval.adversarial_eval import run_adversarial_suite

router = APIRouter(prefix="/eval", tags=["evaluation"])

@router.get("/robustness-report", response_model=RobustnessReport)
def get_robustness_report():
    """Returns the flagship Phase 1 vs Phase 2 adversarial robustness comparison report."""
    return get_latest_robustness_report()

@router.post("/run-benchmark")
def run_benchmark():
    """Triggers an on-demand adversarial benchmark evaluation run across attack tiers."""
    try:
        results = run_adversarial_suite(num_samples_per_attack=3)
        return {
            "status": "completed",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
