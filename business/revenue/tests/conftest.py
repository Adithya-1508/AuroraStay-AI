import uuid
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from backend.models.base import Base
from backend.models.guest import Guest
from backend.models.room import RoomCategory
from backend.repositories.unit_of_work import PostgresUnitOfWork


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Sets up an in-memory SQLite database connection pool for tests."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_maker() as session:
        real_close = session.close

        async def mock_close(*args: Any, **kwargs: Any) -> None:
            pass

        async def mock_rollback(*args: Any, **kwargs: Any) -> None:
            pass

        session.close = mock_close  # type: ignore[method-assign]
        session.rollback = mock_rollback  # type: ignore[method-assign]

        yield session

        await real_close()

    await engine.dispose()


@pytest.fixture(autouse=True)
def mock_uow_session(db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch) -> None:
    """Forces PostgresUnitOfWork to use the in-memory SQLite database session in tests."""
    from backend.repositories.unit_of_work import PostgresUnitOfWork

    old_init = PostgresUnitOfWork.__init__

    def new_init(self: Any, session_factory: Any = None) -> None:
        old_init(self, session_factory=lambda: db_session)  # type: ignore

    monkeypatch.setattr(PostgresUnitOfWork, "__init__", new_init)


@pytest.fixture
async def revenue_setup_data(db_session: AsyncSession) -> dict[str, uuid.UUID]:
    """Sets up a test room category and guest profile."""
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore

    async with uow:
        # 1. Create Room Categories
        cat = RoomCategory(name="Revenue Suite", base_price=200.0)
        cheaper_cat = RoomCategory(name="Standard Room", base_price=100.0)
        await uow.room_categories.add(cat)
        await uow.room_categories.add(cheaper_cat)
        await uow.commit()

        # 2. Create Guest
        guest = Guest(
            first_name="Revenue",
            last_name="Tester",
            email="revenue_tester@hotel.com",
            phone="1234567890",
            loyalty_tier="Gold",
        )
        await uow.guests.add(guest)
        await uow.commit()

        return {
            "room_category_id": cat.id,
            "cheaper_category_id": cheaper_cat.id,
            "guest_id": guest.id,
        }
