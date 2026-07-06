import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, BaseEntity


class Spa(Base, BaseEntity):
    """Spa table mapping database representation."""

    __tablename__ = "spas"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    treatment_type: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    bookings: Mapped[list["SpaBooking"]] = relationship(
        back_populates="spa", cascade="all, delete-orphan"
    )


class SpaBooking(Base, BaseEntity):
    """SpaBooking table mapping database representation."""

    __tablename__ = "spa_bookings"

    guest_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("guests.id"), nullable=False)
    spa_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("spas.id"), nullable=False)
    booking_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="Confirmed", nullable=False)

    spa: Mapped[Spa] = relationship(back_populates="bookings")


__all__ = ["Spa", "SpaBooking"]
