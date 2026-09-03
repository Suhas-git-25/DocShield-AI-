"""
DocShield AI - Async Job Queue Manager
Supports background async inference execution, job status tracking, and polling.
"""

import asyncio
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from ..schemas.document import JobStatus, AnalyzeResponse

class JobQueueManager:
    def __init__(self):
        self._jobs: Dict[str, Dict[str, Any]] = {}

    def create_job(self) -> str:
        job_id = f"job_{uuid.uuid4().hex[:10]}"
        self._jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "result": None,
            "error": None
        }
        return job_id

    def set_processing(self, job_id: str):
        if job_id in self._jobs:
            self._jobs[job_id]["status"] = "processing"

    def complete_job(self, job_id: str, result: AnalyzeResponse):
        if job_id in self._jobs:
            self._jobs[job_id]["status"] = "completed"
            self._jobs[job_id]["result"] = result

    def fail_job(self, job_id: str, error_msg: str):
        if job_id in self._jobs:
            self._jobs[job_id]["status"] = "failed"
            self._jobs[job_id]["error"] = error_msg

    def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        if job_id not in self._jobs:
            return None
        data = self._jobs[job_id]
        return JobStatus(
            job_id=data["job_id"],
            status=data["status"],
            created_at=data["created_at"],
            result=data["result"],
            error=data["error"]
        )

job_queue = JobQueueManager()
