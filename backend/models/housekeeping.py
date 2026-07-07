import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, BaseEntity


class HousekeepingTask(Base, BaseEntity):
    """HousekeepingTask table mapping database representation."""

    __tablename__ = "housekeeping_tasks"

    room_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("rooms.id"), nullable=False, index=True
    )
    assigned_employee_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("employees.id"), nullable=True, index=True
    )
    status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    room = relationship("Room", foreign_keys=[room_id])
    assigned_employee = relationship("Employee", foreign_keys=[assigned_employee_id])

    __mapper_args__ = {"version_id_col": version}


__all__ = ["HousekeepingTask"]
