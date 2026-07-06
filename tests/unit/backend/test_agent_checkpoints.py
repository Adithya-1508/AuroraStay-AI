import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.agents.checkpoints.memory import MemoryCheckpointer
from backend.agents.checkpoints.postgres import PostgresCheckpointer


@pytest.mark.asyncio
async def test_memory_checkpointer() -> None:
    """Verifies in-memory checkpointer save, load, and list methods."""
    cp = MemoryCheckpointer()
    await cp.save("thread-1", "cp-1", {"value": 100})

    state = await cp.load("thread-1", "cp-1")
    assert state == {"value": 100}

    # Load latest
    await cp.save("thread-1", "cp-2", {"value": 200})
    latest = await cp.load("thread-1")
    assert latest == {"value": 200}

    lst = await cp.list_checkpoints("thread-1")
    assert len(lst) == 2


@pytest.mark.asyncio
async def test_postgres_checkpointer() -> None:
    """Verifies PostgreSQL checkpointer using an async SQLite memory engine."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    cp = PostgresCheckpointer(session_maker)

    # Initialize Table
    await cp.initialize_table()

    # Save checkpoint
    await cp.save("thread-x", "cp-a", {"data": "hello"})

    # Load checkpoint
    state = await cp.load("thread-x", "cp-a")
    assert state == {"data": "hello"}

    # Load latest
    await cp.save("thread-x", "cp-b", {"data": "world"})
    latest = await cp.load("thread-x")
    assert latest == {"data": "world"}

    # Clean up resources
    await engine.dispose()
