from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.logging import configure_logger, logger
from backend.core.settings import settings
from backend.database.engine import engine
from backend.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager handling application setup and shutdown hooks."""
    # Startup actions
    configure_logger()
    logger.info("Starting HospitalityAI API services...")

    # Run auto-schema creation in development environment
    db_url = settings.DATABASE_URL.lower()
    is_dev = (
        "localhost" in db_url or "127.0.0.1" in db_url or db_url.startswith("sqlite")
    )
    if is_dev:
        logger.info("Development database detected. Creating missing schema tables...")
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database schema verification completed successfully.")
        except Exception as e:
            logger.error(
                "Failed to verify/create database schema on startup", error=str(e)
            )

    yield

    # Shutdown actions
    logger.info("Stopping HospitalityAI API services...")
