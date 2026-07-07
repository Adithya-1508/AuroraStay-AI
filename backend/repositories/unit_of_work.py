from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.database.session import async_session_factory
from backend.models.employee import Employee
from backend.models.reservation import ReservationHistory
from backend.repositories.postgres.base import PostgresRepository
from backend.repositories.postgres.forecast import ForecastRepository
from backend.repositories.postgres.guest import GuestRepository
from backend.repositories.postgres.housekeeping import HousekeepingRepository
from backend.repositories.postgres.knowledge import KnowledgeRepository
from backend.repositories.postgres.maintenance import MaintenanceRepository
from backend.repositories.postgres.recommendation import RecommendationRepository
from backend.repositories.postgres.reservation import ReservationRepository
from backend.repositories.postgres.review import ReviewRepository
from backend.repositories.postgres.room import (
    RoomCategoryRepository,
    RoomRepository,
)


class AbstractUnitOfWork(ABC):
    """Abstract interface defining the Unit of Work pattern."""

    session: AsyncSession
    guests: GuestRepository
    reservations: ReservationRepository
    reviews: ReviewRepository
    knowledge: KnowledgeRepository
    forecasts: ForecastRepository
    recommendations: RecommendationRepository
    rooms: RoomRepository
    room_categories: RoomCategoryRepository
    reservation_histories: PostgresRepository[ReservationHistory]
    housekeeping: HousekeepingRepository
    maintenance: MaintenanceRepository
    employees: PostgresRepository[Employee]

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Commits changes performed inside transaction context."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollbacks transaction states back to boundaries."""
        pass


class PostgresUnitOfWork(AbstractUnitOfWork):
    """Postgres concrete implementation of the Unit of Work transaction pattern."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = async_session_factory,
    ) -> None:
        self.session_factory = session_factory
        self.session: AsyncSession = None  # type: ignore

    async def __aenter__(self) -> "PostgresUnitOfWork":
        self.session = self.session_factory()
        self.guests = GuestRepository(self.session)
        self.reservations = ReservationRepository(self.session)
        self.reviews = ReviewRepository(self.session)
        self.knowledge = KnowledgeRepository(self.session)
        self.forecasts = ForecastRepository(self.session)
        self.recommendations = RecommendationRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.room_categories = RoomCategoryRepository(self.session)
        self.reservation_histories = PostgresRepository(
            self.session, ReservationHistory
        )
        self.housekeeping = HousekeepingRepository(self.session)
        self.maintenance = MaintenanceRepository(self.session)
        self.employees = PostgresRepository(self.session, Employee)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


__all__ = ["AbstractUnitOfWork", "PostgresUnitOfWork"]
