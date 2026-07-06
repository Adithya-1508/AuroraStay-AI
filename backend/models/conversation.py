import uuid
from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, BaseEntity


class Conversation(Base, BaseEntity):
    """Conversation table mapping database representation."""

    __tablename__ = "conversations"

    guest_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("guests.id"), nullable=True
    )
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    messages: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    __mapper_args__ = {"version_id_col": version}


__all__ = ["Conversation"]
