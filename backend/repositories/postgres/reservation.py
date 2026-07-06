import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.reservation import Reservation
from backend.repositories.postgres.base import PostgresRepository
from backend.repositories.reservation import AbstractReservationRepository


class ReservationRepository(
    PostgresRepository[Reservation], AbstractReservationRepository
):
    """Postgres concrete repository managing Reservation records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Reservation)

    async def get_by_guest(self, guest_id: str) -> Sequence[Reservation]:
        """Retrieves all active reservations associated with a specific guest ID."""
        try:
            uuid_val = uuid.UUID(guest_id)
        except ValueError:
            return []
        stmt = select(Reservation).filter_by(guest_id=uuid_val, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["ReservationRepository"]
