from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator


class ReportIn(BaseModel):
    ngo_id: str = Field(min_length=1, max_length=64)
    month: str = Field(pattern=r"^\d{4}-\d{2}$")
    people_helped: int = Field(ge=0)
    events_conducted: int = Field(ge=0)
    funds_utilized: float = Field(ge=0)

    @field_validator("month")
    @classmethod
    def validate_month(cls, v: str) -> str:
        year_s, month_s = v.split("-")
        year = int(year_s)
        month = int(month_s)
        if year < 1900 or year > 2100:
            raise ValueError("year out of range")
        if month < 1 or month > 12:
            raise ValueError("month out of range")
        return v

    def month_date(self) -> date:
        year_s, month_s = self.month.split("-")
        return date(int(year_s), int(month_s), 1)


class ReportOut(BaseModel):
    ngo_id: str
    month: str
    people_helped: int
    events_conducted: int
    funds_utilized: float

