import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, BaseEntity


class Reservation(Base, BaseEntity):
    """Reservation table mapping database representation."""

    __tablename__ = "reservations"

    guest_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("guests.id"), nullable=False)
    room_category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("room_categories.id"), nullable=False
    )
    assigned_room_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("rooms.id"), nullable=True
    )
    check_in_date: Mapped[date] = mapped_column(Date, nullable=False)
    check_out_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="Pending", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    guest: Mapped["Guest"] = relationship(back_populates="reservations")  # type: ignore  # noqa: F821
    room_category: Mapped["RoomCategory"] = relationship(  # type: ignore  # noqa: F821
        back_populates="reservations"
    )
    assigned_room: Mapped["Room | None"] = relationship(  # type: ignore  # noqa: F821
        back_populates="reservations"
    )
    review: Mapped["Review | None"] = relationship(  # type: ignore  # noqa: F821
        back_populates="reservation", cascade="all, delete-orphan"
    )
    history: Mapped[list["ReservationHistory"]] = relationship(
        back_populates="reservation", cascade="all, delete-orphan"
    )

    __mapper_args__ = {"version_id_col": version}


class ReservationHistory(Base, BaseEntity):
    """Tracks audit logs of status transitions and changes to reservations."""

    __tablename__ = "reservation_history"

    reservation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("reservations.id"), nullable=False
    )
    old_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    new_status: Mapped[str] = mapped_column(String(50), nullable=False)
    changed_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    reservation: Mapped[Reservation] = relationship(back_populates="history")


__all__ = ["Reservation", "ReservationHistory"]
