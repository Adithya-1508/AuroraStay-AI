from datetime import date, datetime

from sqlalchemy import Date, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, BaseEntity


class Forecast(Base, BaseEntity):
    """Forecast table mapping database representation."""

    __tablename__ = "forecasts"

    target_date: Mapped[date] = mapped_column(Date, nullable=False)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    predicted_value: Mapped[float] = mapped_column(Numeric(12, 4), nullable=False)
    confidence_lower: Mapped[float | None] = mapped_column(
        Numeric(12, 4), nullable=True
    )
    confidence_upper: Mapped[float | None] = mapped_column(
        Numeric(12, 4), nullable=True
    )
    forecast_generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


__all__ = ["Forecast"]
