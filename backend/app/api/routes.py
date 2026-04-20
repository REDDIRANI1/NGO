from fastapi import APIRouter

from app.api.dashboard import router as dashboard_router
from app.api.job_status import router as job_status_router
from app.api.report import router as report_router
from app.api.reports_upload import router as reports_upload_router

router = APIRouter()

router.include_router(report_router)
router.include_router(dashboard_router)
router.include_router(reports_upload_router)
router.include_router(job_status_router)


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}

