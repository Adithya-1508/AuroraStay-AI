import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, BaseEntity


class Review(Base, BaseEntity):
    """Review table mapping database representation."""

    __tablename__ = "reviews"

    reservation_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("reservations.id"), unique=True, nullable=True
    )
    guest_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("guests.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    sentiment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    guest: Mapped["Guest"] = relationship(back_populates="reviews")  # type: ignore  # noqa: F821
    reservation: Mapped["Reservation | None"] = relationship(  # type: ignore  # noqa: F821
        back_populates="review"
    )

    __mapper_args__ = {"version_id_col": version}


__all__ = ["Review"]
