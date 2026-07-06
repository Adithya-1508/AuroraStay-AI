import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.review import Review
from backend.repositories.postgres.base import PostgresRepository
from backend.repositories.review import AbstractReviewRepository


class ReviewRepository(PostgresRepository[Review], AbstractReviewRepository):
    """Postgres concrete repository managing Review records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Review)

    async def get_by_guest(self, guest_id: str) -> Sequence[Review]:
        """Retrieves all active reviews submitted by a specific guest ID."""
        try:
            uuid_val = uuid.UUID(guest_id)
        except ValueError:
            return []
        stmt = select(Review).filter_by(guest_id=uuid_val, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["ReviewRepository"]
