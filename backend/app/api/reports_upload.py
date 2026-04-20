from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery_app import celery_app
from app.db import get_db
from app.models import Job


router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/upload")
async def upload_reports_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> dict:
    contents = await file.read()
    csv_text = contents.decode("utf-8", errors="replace")

    job = Job(
        id=uuid.uuid4(),
        type="csv_upload",
        status="queued",
        total_rows=0,
        processed_rows=0,
        succeeded_rows=0,
        failed_rows=0,
        csv_text=csv_text,
    )
    db.add(job)
    await db.commit()

    celery_app.send_task("jobs.process_csv_job", args=[str(job.id)])

    return {"job_id": str(job.id)}

