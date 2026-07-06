from typing import Any

from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, BaseEntity


class Guest(Base, BaseEntity):
    """Guest table mapping database representation."""

    __tablename__ = "guests"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    loyalty_tier: Mapped[str] = mapped_column(
        String(50), default="Bronze", nullable=False
    )
    preferences: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="guest", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="guest", cascade="all, delete-orphan"
    )

    __mapper_args__ = {"version_id_col": version}


__all__ = ["Guest"]
