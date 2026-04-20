"""create reports table

Revision ID: 20260420_01
Revises: 
Create Date: 2026-04-20
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "20260420_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("ngo_id", sa.String(length=64), nullable=False),
        sa.Column("month", sa.Date(), nullable=False),
        sa.Column("people_helped", sa.Integer(), nullable=False),
        sa.Column("events_conducted", sa.Integer(), nullable=False),
        sa.Column("funds_utilized", sa.Numeric(14, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("ngo_id", "month", name="uq_reports_ngo_month"),
    )
    op.create_index("ix_reports_ngo_id", "reports", ["ngo_id"])
    op.create_index("ix_reports_month", "reports", ["month"])


def downgrade() -> None:
    op.drop_index("ix_reports_month", table_name="reports")
    op.drop_index("ix_reports_ngo_id", table_name="reports")
    op.drop_table("reports")

