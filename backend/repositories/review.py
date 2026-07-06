from abc import ABC, abstractmethod
from collections.abc import Sequence

from backend.models.base import BaseEntity
from backend.repositories.base import AbstractRepository


class AbstractReviewRepository(AbstractRepository[BaseEntity], ABC):
    """Abstract interface defining behaviors for Review persistence."""

    @abstractmethod
    async def get_by_guest(self, guest_id: str) -> Sequence[BaseEntity]:
        """Retrieves all reviews submitted by a specific guest ID."""
        pass


__all__ = ["AbstractReviewRepository"]
