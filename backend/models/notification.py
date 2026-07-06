import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, BaseEntity


class Notification(Base, BaseEntity):
    """Notification table mapping database representation."""

    __tablename__ = "notifications"

    guest_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("guests.id"), nullable=True
    )
    employee_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("employees.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __mapper_args__ = {"version_id_col": version}


__all__ = ["Notification"]
