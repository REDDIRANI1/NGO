from __future__ import annotations

import asyncio
import csv
import uuid
from io import StringIO

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.celery_app import celery_app
from app.db import SessionLocal
from app.models import Job, JobItem, Report
from app.schemas.report import ReportIn


@celery_app.task(name="jobs.noop")
def noop() -> dict:
    return {"ok": True}


@celery_app.task(name="jobs.process_csv_job")
def process_csv_job(job_id: str) -> dict:
    return asyncio.run(_process_csv_job(job_id))


async def _process_csv_job(job_id: str) -> dict:
    job_uuid = uuid.UUID(job_id)
    async with SessionLocal() as db:
        job = (await db.execute(select(Job).where(Job.id == job_uuid))).scalar_one_or_none()
        if job is None:
            return {"ok": False, "error": "job not found"}

        job.status = "processing"
        job.processed_rows = 0
        job.succeeded_rows = 0
        job.failed_rows = 0
        await db.commit()

        f = StringIO(job.csv_text)
        reader = csv.DictReader(f)

        processed = 0
        succeeded = 0
        failed = 0
        total = 0

        # Row numbers: 1 is header; start data at 2.
        for i, row in enumerate(reader, start=2):
            total += 1
            processed += 1
            payload = {k: (v.strip() if isinstance(v, str) else v) for k, v in (row or {}).items()}

            try:
                report_in = ReportIn(
                    ngo_id=str(payload.get("ngo_id") or "").strip(),
                    month=str(payload.get("month") or "").strip(),
                    people_helped=int(payload.get("people_helped") or 0),
                    events_conducted=int(payload.get("events_conducted") or 0),
                    funds_utilized=float(payload.get("funds_utilized") or 0),
                )
            except Exception as e:  # validation errors
                db.add(
                    JobItem(
                        job_id=job.id,
                        row_number=i,
                        status="failed",
                        error=str(e),
                        payload=payload,
                    )
                )
                failed += 1
                job.failed_rows = failed
                job.processed_rows = processed
                job.total_rows = total
                await db.commit()
                continue

            month_date = report_in.month_date()
            stmt = (
                insert(Report)
                .values(
                    ngo_id=report_in.ngo_id,
                    month=month_date,
                    people_helped=report_in.people_helped,
                    events_conducted=report_in.events_conducted,
                    funds_utilized=report_in.funds_utilized,
                )
                .on_conflict_do_update(
                    constraint="uq_reports_ngo_month",
                    set_={
                        "people_helped": report_in.people_helped,
                        "events_conducted": report_in.events_conducted,
                        "funds_utilized": report_in.funds_utilized,
                    },
                )
            )

            try:
                await db.execute(stmt)
                db.add(JobItem(job_id=job.id, row_number=i, status="succeeded", payload=payload))
                succeeded += 1
            except Exception as e:
                db.add(
                    JobItem(
                        job_id=job.id,
                        row_number=i,
                        status="failed",
                        error=str(e),
                        payload=payload,
                    )
                )
                failed += 1

            job.total_rows = total
            job.processed_rows = processed
            job.succeeded_rows = succeeded
            job.failed_rows = failed
            await db.commit()

        job.status = "completed_with_errors" if failed > 0 else "completed"
        job.total_rows = total
        job.processed_rows = processed
        job.succeeded_rows = succeeded
        job.failed_rows = failed
        await db.commit()

        return {
            "ok": True,
            "job_id": str(job.id),
            "total_rows": total,
            "succeeded_rows": succeeded,
            "failed_rows": failed,
        }

