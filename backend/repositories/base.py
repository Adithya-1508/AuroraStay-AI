from abc import ABC, abstractmethod
from collections.abc import Sequence

from backend.models.base import BaseEntity


class AbstractRepository[T: BaseEntity](ABC):
    """Abstract interface defining standard CRUD behaviors for repositories."""

    @abstractmethod
    async def get(self, entity_id: str) -> T | None:
        """Retrieves an entity by its identifier."""
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[T]:
        """Retrieves a list of all active entities."""
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Saves a new entity into the database."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Updates attributes of an existing entity."""
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Removes (or soft deletes) an entity from the database."""
        pass


__all__ = ["AbstractRepository"]
