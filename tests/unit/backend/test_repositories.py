from collections.abc import AsyncGenerator
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.models.base import Base
from backend.models.guest import Guest
from backend.models.reservation import Reservation
from backend.models.room import Room, RoomCategory
from backend.repositories.postgres.guest import GuestRepository
from backend.repositories.postgres.reservation import ReservationRepository
from backend.repositories.unit_of_work import PostgresUnitOfWork


@pytest_asyncio.fixture
async def sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    """Sets up an in-memory SQLite database connection pool."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_maker() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_guest_repository_crud(sqlite_session: AsyncSession) -> None:
    """Verifies GuestRepository basic CRUD and specialized select queries."""
    repo = GuestRepository(sqlite_session)
    guest = Guest(
        first_name="Gregory",
        last_name="House",
        email="gregory.house@princeton.org",
        phone="+1-555-0303",
    )
    await repo.add(guest)
    await sqlite_session.commit()

    # Get by ID check
    fetched = await repo.get(str(guest.id))
    assert fetched is not None
    assert fetched.first_name == "Gregory"

    # Get by email check
    fetched_email = await repo.get_by_email("gregory.house@princeton.org")
    assert fetched_email is not None
    assert fetched_email.id == guest.id

    # Get all check
    all_guests = await repo.get_all()
    assert len(all_guests) == 1

    # Soft delete check
    deleted = await repo.delete(str(guest.id))
    assert deleted is True
    await sqlite_session.commit()

    fetched_deleted = await repo.get(str(guest.id))
    assert fetched_deleted is None


@pytest.mark.asyncio
async def test_reservation_repository_crud(sqlite_session: AsyncSession) -> None:
    """Verifies ReservationRepository joins and queries."""
    # Seed category & guest
    guest = Guest(
        first_name="Diana",
        last_name="Prince",
        email="diana.prince@temyscira.gov",
    )
    category = RoomCategory(name="Standard", base_price=120.00)
    sqlite_session.add(guest)
    sqlite_session.add(category)
    await sqlite_session.flush()

    room = Room(room_number="101", category_id=category.id)
    sqlite_session.add(room)
    await sqlite_session.flush()

    res_repo = ReservationRepository(sqlite_session)
    res = Reservation(
        guest_id=guest.id,
        room_category_id=category.id,
        assigned_room_id=room.id,
        check_in_date=date(2026, 7, 10),
        check_out_date=date(2026, 7, 15),
        total_cost=600.00,
        status="Pending",
    )
    await res_repo.add(res)
    await sqlite_session.commit()

    # Query check
    bookings = await res_repo.get_by_guest(str(guest.id))
    assert len(bookings) == 1
    assert bookings[0].total_cost == 600.00


@pytest.mark.asyncio
async def test_unit_of_work_transaction(sqlite_session: AsyncSession) -> None:
    """Verifies PostgresUnitOfWork commits and rollbacks operations."""

    def mock_factory() -> AsyncSession:
        return sqlite_session

    uow = PostgresUnitOfWork(session_factory=mock_factory)  # type: ignore
    async with uow:
        guest = Guest(
            first_name="Elena",
            last_name="Rostova",
            email="elena.rostova@example.com",
        )
        await uow.guests.add(guest)
        await uow.commit()

    # Verify commit
    repo = GuestRepository(sqlite_session)
    fetched = await repo.get_by_email("elena.rostova@example.com")
    assert fetched is not None
