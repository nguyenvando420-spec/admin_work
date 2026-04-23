from typing import Any
from fastapi import APIRouter, Depends
from app.dependencies.permission import require_permission

router = APIRouter()

@router.get("/items", dependencies=[Depends(require_permission("job_monitor", "view"))])
def get_job_items() -> Any:
    return {"items": [{"jobId": 1, "status": "running"}]}

@router.post("/run", dependencies=[Depends(require_permission("job_monitor", "fore"))])
def run_job() -> Any:
    return {"message": "Job executed successfully"}
