from typing import Any
from uuid import UUID

from backend.models.room import Room
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.reservation.availability.engine import AvailabilityEngine
from business.reservation.domain.value_objects import BookingWindow


class AvailabilityService:
    """Application Service wrapping availability checking logic."""

    def __init__(self, engine: AvailabilityEngine | None = None) -> None:
        self.engine = engine or AvailabilityEngine()

    async def check_category_availability(
        self, uow: AbstractUnitOfWork, category_id: UUID, window: BookingWindow
    ) -> bool:
        """Determines if a room category is available for booking dates."""
        return await self.engine.check_category_availability(uow, category_id, window)

    async def get_available_rooms(
        self,
        uow: AbstractUnitOfWork,
        window: BookingWindow,
        category_id: UUID | None = None,
        preferences: dict[str, Any] | None = None,
    ) -> list[Room]:
        """Retrieves list of free physical rooms."""
        return await self.engine.get_available_rooms(
            uow, window, category_id=category_id, preferences=preferences
        )

    async def suggest_alternatives(
        self,
        uow: AbstractUnitOfWork,
        requested_category_id: UUID,
        window: BookingWindow,
    ) -> list[dict[str, Any]]:
        """Suggests alternative booking dates or categories."""
        return await self.engine.suggest_alternatives(
            uow, requested_category_id, window
        )


__all__ = ["AvailabilityService"]
