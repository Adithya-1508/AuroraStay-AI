from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.forecast import Forecast
from backend.repositories.forecast import AbstractForecastRepository
from backend.repositories.postgres.base import PostgresRepository


class ForecastRepository(PostgresRepository[Forecast], AbstractForecastRepository):
    """Postgres concrete repository managing Forecast records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Forecast)

    async def get_by_metric(self, metric_name: str) -> Sequence[Forecast]:
        """Retrieves all active forecasts associated with a specific metric name."""
        stmt = select(Forecast).filter_by(metric_name=metric_name, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["ForecastRepository"]
