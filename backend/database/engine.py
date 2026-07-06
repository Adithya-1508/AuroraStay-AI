from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from backend.core.settings import settings


def get_async_db_url(url: str) -> str:
    """Modifies the connection URL to enforce async dialect drivers."""
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    return url


# Initialize database engine with pool parameters
engine: AsyncEngine = create_async_engine(
    get_async_db_url(settings.DATABASE_URL),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

__all__ = ["engine", "get_async_db_url"]
