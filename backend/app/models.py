import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (UniqueConstraint("ngo_id", "month", name="uq_reports_ngo_month"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ngo_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    month: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    people_helped: Mapped[int] = mapped_column(Integer, nullable=False)
    events_conducted: Mapped[int] = mapped_column(Integer, nullable=False)
    funds_utilized: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

