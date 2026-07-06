from typing import Any
from uuid import UUID

from backend.models.room import Room
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.reservation.allocation.engine import AllocationEngine


class AllocationService:
    """Application Service wrapping room allocation and releasing operations."""

    def __init__(self, engine: AllocationEngine | None = None) -> None:
        self.engine = engine or AllocationEngine()

    async def allocate_room(
        self,
        uow: AbstractUnitOfWork,
        reservation_id: UUID,
        preferences: dict[str, Any] | None = None,
    ) -> Room:
        """Assigns physical room to reservation booking."""
        return await self.engine.allocate_room(uow, reservation_id, preferences)

    async def release_room_allocation(
        self, uow: AbstractUnitOfWork, reservation_id: UUID
    ) -> None:
        """Removes room assignment from reservation booking."""
        await self.engine.release_room_allocation(uow, reservation_id)


__all__ = ["AllocationService"]
