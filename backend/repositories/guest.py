from abc import abstractmethod

from backend.models.base import BaseEntity
from backend.repositories.base import AbstractRepository


class AbstractGuestRepository(AbstractRepository[BaseEntity]):
    """Abstract interface defining behaviors for Guest CRM persistence."""

    @abstractmethod
    async def get_by_email(self, email: str) -> BaseEntity | None:
        """Retrieves a guest record utilizing their contact email address."""
        pass


__all__ = ["AbstractGuestRepository"]
