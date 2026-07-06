import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.room import Room, RoomCategory
from backend.repositories.postgres.base import PostgresRepository
from backend.repositories.room import (
    AbstractRoomCategoryRepository,
    AbstractRoomRepository,
)


class RoomCategoryRepository(
    PostgresRepository[RoomCategory], AbstractRoomCategoryRepository
):
    """Postgres concrete repository managing RoomCategory records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RoomCategory)

    async def get_by_name(self, name: str) -> RoomCategory | None:
        stmt = select(RoomCategory).filter_by(name=name, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


class RoomRepository(PostgresRepository[Room], AbstractRoomRepository):
    """Postgres concrete repository managing Room records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Room)

    async def get_by_room_number(self, room_number: str) -> Room | None:
        stmt = select(Room).filter_by(room_number=room_number, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_category(self, category_id: str) -> Sequence[Room]:
        try:
            uuid_val = uuid.UUID(category_id)
        except ValueError:
            return []
        stmt = select(Room).filter_by(category_id=uuid_val, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["RoomCategoryRepository", "RoomRepository"]
