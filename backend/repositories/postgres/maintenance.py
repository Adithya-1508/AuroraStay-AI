from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.maintenance import MaintenanceRequest
from backend.repositories.maintenance import AbstractMaintenanceRepository
from backend.repositories.postgres.base import PostgresRepository


class MaintenanceRepository(
    PostgresRepository[MaintenanceRequest], AbstractMaintenanceRepository
):
    """Postgres concrete repository managing MaintenanceRequest records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MaintenanceRequest)

    async def get_by_room(self, room_id: str) -> Sequence[MaintenanceRequest]:
        """Retrieves maintenance requests logged for a specific room."""
        try:
            uuid_val = UUID(room_id)
        except ValueError:
            return []
        stmt = select(MaintenanceRequest).filter_by(room_id=uuid_val, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["MaintenanceRepository"]
