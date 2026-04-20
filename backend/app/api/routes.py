from fastapi import APIRouter

from app.api.report import router as report_router

router = APIRouter()

router.include_router(report_router)


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}

