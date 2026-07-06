from abc import ABC, abstractmethod
from collections.abc import Sequence

from backend.models.base import BaseEntity
from backend.repositories.base import AbstractRepository


class AbstractKnowledgeRepository(AbstractRepository[BaseEntity], ABC):
    """Abstract interface defining behaviors for KnowledgeDocument persistence."""

    @abstractmethod
    async def get_by_category(self, category: str) -> Sequence[BaseEntity]:
        """Retrieves all knowledge documents registered under a specific category."""
        pass


__all__ = ["AbstractKnowledgeRepository"]
