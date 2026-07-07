from abc import abstractmethod
from collections.abc import Sequence

from backend.models.housekeeping import HousekeepingTask
from backend.repositories.base import AbstractRepository


class AbstractHousekeepingRepository(AbstractRepository[HousekeepingTask]):
    """Abstract interface defining behaviors for HousekeepingTask persistence."""

    @abstractmethod
    async def get_by_room(self, room_id: str) -> Sequence[HousekeepingTask]:
        """Retrieves housekeeping tasks assigned to a specific room."""
        pass


__all__ = ["AbstractHousekeepingRepository"]
