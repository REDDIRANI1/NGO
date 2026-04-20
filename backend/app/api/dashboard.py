from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Report
from app.schemas.dashboard import DashboardOut


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def parse_month(month: str) -> date:
    year_s, month_s = month.split("-")
    year = int(year_s)
    month_i = int(month_s)
    return date(year, month_i, 1)


@router.get("", response_model=DashboardOut)
async def get_dashboard(
    month: str = Query(pattern=r"^\d{4}-\d{2}$"),
    db: AsyncSession = Depends(get_db),
) -> DashboardOut:
    month_date = parse_month(month)

    stmt = (
        select(
            func.count(func.distinct(Report.ngo_id)).label("total_ngos_reporting"),
            func.coalesce(func.sum(Report.people_helped), 0).label("total_people_helped"),
            func.coalesce(func.sum(Report.events_conducted), 0).label("total_events_conducted"),
            func.coalesce(func.sum(Report.funds_utilized), 0).label("total_funds_utilized"),
        )
        .select_from(Report)
        .where(Report.month == month_date)
    )

    row = (await db.execute(stmt)).one()

    return DashboardOut(
        month=month,
        total_ngos_reporting=int(row.total_ngos_reporting or 0),
        total_people_helped=int(row.total_people_helped or 0),
        total_events_conducted=int(row.total_events_conducted or 0),
        total_funds_utilized=float(row.total_funds_utilized or 0),
    )

