from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Report
from app.schemas.report import ReportIn, ReportOut


router = APIRouter(prefix="/report", tags=["report"])


@router.post("", response_model=ReportOut)
async def create_report(payload: ReportIn, db: AsyncSession = Depends(get_db)) -> ReportOut:
    month_date = payload.month_date()

    stmt = (
        insert(Report)
        .values(
            ngo_id=payload.ngo_id,
            month=month_date,
            people_helped=payload.people_helped,
            events_conducted=payload.events_conducted,
            funds_utilized=payload.funds_utilized,
        )
        .on_conflict_do_update(
            constraint="uq_reports_ngo_month",
            set_={
                "people_helped": payload.people_helped,
                "events_conducted": payload.events_conducted,
                "funds_utilized": payload.funds_utilized,
            },
        )
        .returning(
            Report.ngo_id,
            Report.month,
            Report.people_helped,
            Report.events_conducted,
            Report.funds_utilized,
        )
    )

    result = await db.execute(stmt)
    await db.commit()

    row = result.one()
    return ReportOut(
        ngo_id=row.ngo_id,
        month=row.month.strftime("%Y-%m"),
        people_helped=row.people_helped,
        events_conducted=row.events_conducted,
        funds_utilized=float(row.funds_utilized),
    )

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Report
from app.schemas.report import ReportIn, ReportOut


router = APIRouter(prefix="/report", tags=["report"])


@router.post("", response_model=ReportOut)
async def create_report(payload: ReportIn, db: AsyncSession = Depends(get_db)) -> ReportOut:
    month_date = payload.month_date()

    stmt = (
        insert(Report)
        .values(
            ngo_id=payload.ngo_id,
            month=month_date,
            people_helped=payload.people_helped,
            events_conducted=payload.events_conducted,
            funds_utilized=payload.funds_utilized,
        )
        .on_conflict_do_update(
            constraint="uq_reports_ngo_month",
            set_={
                "people_helped": payload.people_helped,
                "events_conducted": payload.events_conducted,
                "funds_utilized": payload.funds_utilized,
            },
        )
        .returning(
            Report.ngo_id,
            Report.month,
            Report.people_helped,
            Report.events_conducted,
            Report.funds_utilized,
        )
    )

    result = await db.execute(stmt)
    await db.commit()

    row = result.one()
    return ReportOut(
        ngo_id=row.ngo_id,
        month=row.month.strftime("%Y-%m"),
        people_helped=row.people_helped,
        events_conducted=row.events_conducted,
        funds_utilized=float(row.funds_utilized),
    )

