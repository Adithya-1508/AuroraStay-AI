import uuid

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, BaseEntity


class RoomCategory(Base, BaseEntity):
    """RoomCategory table mapping database representation."""

    __tablename__ = "room_categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    base_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    rooms: Mapped[list["Room"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )
    reservations: Mapped[list["Reservation"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="room_category"
    )


class Room(Base, BaseEntity):
    """Room table mapping database representation."""

    __tablename__ = "rooms"

    room_number: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("room_categories.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="Available", nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    category: Mapped[RoomCategory] = relationship(back_populates="rooms")
    reservations: Mapped[list["Reservation"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="assigned_room"
    )

    __mapper_args__ = {"version_id_col": version}


__all__ = ["RoomCategory", "Room"]
