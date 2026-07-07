from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.housekeeping import HousekeepingTask
from backend.repositories.housekeeping import AbstractHousekeepingRepository
from backend.repositories.postgres.base import PostgresRepository


class HousekeepingRepository(
    PostgresRepository[HousekeepingTask], AbstractHousekeepingRepository
):
    """Postgres concrete repository managing HousekeepingTask records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, HousekeepingTask)

    async def get_by_room(self, room_id: str) -> Sequence[HousekeepingTask]:
        """Retrieves housekeeping tasks assigned to a specific room."""
        try:
            uuid_val = UUID(room_id)
        except ValueError:
            return []
        stmt = select(HousekeepingTask).filter_by(room_id=uuid_val, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["HousekeepingRepository"]
