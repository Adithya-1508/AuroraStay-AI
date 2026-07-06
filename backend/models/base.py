import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """SQLAlchemy Declarative Base class."""

    pass


class UUIDMixin:
    """Mixin adding unique UUID identifiers to database tables."""

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    """Mixin adding creation and modification timestamp columns."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """Mixin adding status flags and timestamps for logical deletes."""

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def soft_delete(self) -> None:
        """Transitions record state to logically deleted."""
        self.is_deleted = True
        self.deleted_at = datetime.now(UTC)


class AuditMixin:
    """Mixin adding operator identifiers fields for tracking audits."""

    created_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String(100), nullable=True)


class BaseEntity(UUIDMixin, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Unified base entity with UUID, timestamps, soft delete, and audit."""

    pass


__all__ = [
    "Base",
    "UUIDMixin",
    "TimestampMixin",
    "SoftDeleteMixin",
    "AuditMixin",
    "BaseEntity",
]
