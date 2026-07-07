from abc import abstractmethod
from collections.abc import Sequence

from backend.models.maintenance import MaintenanceRequest
from backend.repositories.base import AbstractRepository


class AbstractMaintenanceRepository(AbstractRepository[MaintenanceRequest]):
    """Abstract interface defining behaviors for MaintenanceRequest persistence."""

    @abstractmethod
    async def get_by_room(self, room_id: str) -> Sequence[MaintenanceRequest]:
        """Retrieves maintenance requests logged for a specific room."""
        pass


__all__ = ["AbstractMaintenanceRepository"]
