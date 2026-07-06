from abc import abstractmethod
from collections.abc import Sequence

from backend.models.base import BaseEntity
from backend.repositories.base import AbstractRepository


class AbstractReservationRepository(AbstractRepository[BaseEntity]):
    """Abstract interface defining behaviors for Reservation persistence."""

    @abstractmethod
    async def get_by_guest(self, guest_id: str) -> Sequence[BaseEntity]:
        """Retrieves all reservations registered for a specific guest ID."""
        pass


__all__ = ["AbstractReservationRepository"]
