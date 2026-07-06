from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from backend.models.base import Base


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
        # Prevent premature session close from destroying in-memory database
        real_close = session.close

        async def mock_close(*args: Any, **kwargs: Any) -> None:
            pass

        session.close = mock_close  # type: ignore[method-assign]

        yield session

        await real_close()

    await engine.dispose()
