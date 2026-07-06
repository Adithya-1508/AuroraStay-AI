from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, BaseEntity


class ETLExecution(Base, BaseEntity):
    """ETLExecution table mapping database representation."""

    __tablename__ = "etl_executions"

    dataset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    dataset_version: Mapped[str] = mapped_column(String(50), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    row_counts: Mapped[int] = mapped_column(Integer, nullable=False)
    validation_status: Mapped[str] = mapped_column(String(50), nullable=False)
    execution_duration_sec: Mapped[float] = mapped_column(
        Numeric(10, 3), nullable=False
    )
    error_report: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


__all__ = ["ETLExecution"]
