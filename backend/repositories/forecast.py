from abc import ABC, abstractmethod
from collections.abc import Sequence

from backend.models.base import BaseEntity
from backend.repositories.base import AbstractRepository


class AbstractForecastRepository(AbstractRepository[BaseEntity], ABC):
    """Abstract interface defining behaviors for Forecast persistence."""

    @abstractmethod
    async def get_by_metric(self, metric_name: str) -> Sequence[BaseEntity]:
        """Retrieves all forecasts associated with a specific metric name."""
        pass


__all__ = ["AbstractForecastRepository"]
