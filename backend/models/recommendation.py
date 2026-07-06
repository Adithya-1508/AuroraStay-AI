import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, BaseEntity


class Recommendation(Base, BaseEntity):
    """Recommendation table mapping database representation."""

    __tablename__ = "recommendations"

    guest_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("guests.id"), nullable=False)
    item_type: Mapped[str] = mapped_column(String(100), nullable=False)
    item_reference_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    score: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)
    is_accepted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )


__all__ = ["Recommendation"]
