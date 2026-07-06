from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.base import BaseEntity
from backend.repositories.base import AbstractRepository


class PostgresRepository[T: BaseEntity](AbstractRepository[T]):
    """Generic concrete implementation of the Repository pattern using SQLAlchemy."""

    def __init__(self, session: AsyncSession, model_class: type[T]) -> None:
        self.session = session
        self.model_class = model_class

    async def get(self, entity_id: str) -> T | None:
        """Retrieves an active (non-deleted) entity by its unique UUID string."""
        try:
            uuid_val = UUID(entity_id)
        except ValueError:
            return None
        stmt = select(self.model_class).filter_by(id=uuid_val, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[T]:
        """Retrieves all active (non-deleted) entities."""
        stmt = select(self.model_class).filter_by(is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, entity: T) -> T:
        """Adds a new entity record into the transaction session context."""
        self.session.add(entity)
        return entity

    async def update(self, entity: T) -> T:
        """Marks the entity to track attributes updates on session commit."""
        # SQLAlchemy handles dirty tracking inside session. No extra commands needed.
        return entity

    async def delete(self, entity_id: str) -> bool:
        """Applies soft delete by setting is_deleted=True and updating deleted_at."""
        entity = await self.get(entity_id)
        if entity:
            entity.soft_delete()
            return True
        return False


__all__ = ["PostgresRepository"]
