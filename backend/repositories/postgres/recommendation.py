import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.recommendation import Recommendation
from backend.repositories.postgres.base import PostgresRepository
from backend.repositories.recommendation import AbstractRecommendationRepository


class RecommendationRepository(
    PostgresRepository[Recommendation], AbstractRecommendationRepository
):
    """Postgres concrete repository managing Recommendation records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Recommendation)

    async def get_by_guest(self, guest_id: str) -> Sequence[Recommendation]:
        """Retrieves all active recommendations associated with a specific guest ID."""
        try:
            uuid_val = uuid.UUID(guest_id)
        except ValueError:
            return []
        stmt = select(Recommendation).filter_by(guest_id=uuid_val, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["RecommendationRepository"]
