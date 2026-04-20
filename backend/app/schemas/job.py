from __future__ import annotations

from pydantic import BaseModel


class JobItemFailure(BaseModel):
    row_number: int
    error: str


class JobStatusOut(BaseModel):
    job_id: str
    status: str
    total_rows: int
    processed_rows: int
    succeeded_rows: int
    failed_rows: int
    failures: list[JobItemFailure] = []

