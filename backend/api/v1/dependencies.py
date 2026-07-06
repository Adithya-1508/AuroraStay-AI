from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import get_db_session
from backend.repositories.guest import AbstractGuestRepository
from backend.repositories.postgres.guest import GuestRepository
from backend.repositories.postgres.reservation import ReservationRepository
from backend.repositories.reservation import AbstractReservationRepository
from backend.repositories.unit_of_work import PostgresUnitOfWork


def get_unit_of_work() -> PostgresUnitOfWork:
    """Dependency injector resolving concrete PostgresUnitOfWork transactions."""
    return PostgresUnitOfWork()


def get_guest_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractGuestRepository:
    """Dependency injector resolving concrete guest repositories."""
    return GuestRepository(session)


def get_reservation_repository(
    session: AsyncSession = Depends(get_db_session),
) -> AbstractReservationRepository:
    """Dependency injector resolving concrete reservation repositories."""
    return ReservationRepository(session)


__all__ = ["get_unit_of_work", "get_guest_repository", "get_reservation_repository"]
