import asyncio
from collections.abc import Generator

import pytest

from shared.config import Settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Creates a session-wide event loop for running async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Returns an isolated Settings object for test overrides."""
    return Settings(
        DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/hospitality_test",
        REDIS_URL="redis://localhost:6379/1",  # Use db 1 for testing
        LOG_LEVEL="WARNING",
    )
