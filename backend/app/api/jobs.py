"""
DocShield AI - Jobs API
Polls status and retrieves results of asynchronous analysis jobs.
"""

from fastapi import APIRouter, HTTPException
from ..schemas.document import JobStatus
from ..services.job_queue import job_queue

router = APIRouter(prefix="/documents/jobs", tags=["jobs"])

@router.get("/{job_id}", response_model=JobStatus)
def get_job_status(job_id: str):
    """Polls async job status."""
    status = job_queue.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found.")
    return status
