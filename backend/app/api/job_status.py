from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Job, JobItem
from app.schemas.job import JobItemFailure, JobStatusOut


router = APIRouter(prefix="/job-status", tags=["jobs"])


@router.get("/{job_id}", response_model=JobStatusOut)
async def get_job_status(job_id: str, db: AsyncSession = Depends(get_db)) -> JobStatusOut:
    try:
        job_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job_id")

    job = (await db.execute(select(Job).where(Job.id == job_uuid))).scalar_one_or_none()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    failures_rows = (
        await db.execute(
            select(JobItem.row_number, JobItem.error)
            .where(JobItem.job_id == job_uuid, JobItem.status == "failed")
            .order_by(JobItem.row_number.asc())
            .limit(20)
        )
    ).all()

    failures = [JobItemFailure(row_number=r[0], error=r[1] or "Invalid row") for r in failures_rows]

    return JobStatusOut(
        job_id=str(job.id),
        status=job.status,
        total_rows=job.total_rows,
        processed_rows=job.processed_rows,
        succeeded_rows=job.succeeded_rows,
        failed_rows=job.failed_rows,
        failures=failures,
    )

