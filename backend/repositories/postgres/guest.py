from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.guest import Guest
from backend.repositories.guest import AbstractGuestRepository
from backend.repositories.postgres.base import PostgresRepository


class GuestRepository(PostgresRepository[Guest], AbstractGuestRepository):
    """Postgres concrete repository managing Guest records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Guest)

    async def get_by_email(self, email: str) -> Guest | None:
        """Retrieves an active Guest profile using their email address."""
        stmt = select(Guest).filter_by(email=email.strip().lower(), is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


__all__ = ["GuestRepository"]
