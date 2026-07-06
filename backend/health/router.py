import socket
from typing import Any
from urllib.parse import urlparse

from fastapi import APIRouter

from backend.core.settings import settings

router = APIRouter()


def check_tcp_port(host: str, port: int) -> bool:
    """Attempts to open a connection to check host/port status."""
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except Exception:
        return False


def parse_host_port(url: str, default_port: int) -> tuple[str, int]:
    """Extracts host and port from a connection string URL."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "localhost"
        port = parsed.port or default_port
        return host, port
    except Exception:
        return "localhost", default_port


@router.get("/health")
async def health() -> dict[str, Any]:
    """Status checker for database, redis, and qdrant connectivity."""
    db_host, db_port = parse_host_port(settings.DATABASE_URL, 5432)
    redis_host, redis_port = parse_host_port(settings.REDIS_URL, 6379)
    qdrant_host, qdrant_port = parse_host_port(settings.QDRANT_URL, 6333)

    db_ok = check_tcp_port(db_host, db_port)
    redis_ok = check_tcp_port(redis_host, redis_port)
    qdrant_ok = check_tcp_port(qdrant_host, qdrant_port)

    overall = "HEALTHY" if (db_ok and redis_ok and qdrant_ok) else "DEGRADED"

    return {
        "status": overall,
        "details": {
            "database": "UP" if db_ok else "DOWN",
            "redis": "UP" if redis_ok else "DOWN",
            "qdrant": "UP" if qdrant_ok else "DOWN",
            "llm_provider": settings.MODEL_PROVIDER,
        },
    }


@router.get("/ready")
async def ready() -> dict[str, Any]:
    """Readiness endpoint verifying core databases readiness state."""
    db_host, db_port = parse_host_port(settings.DATABASE_URL, 5432)
    db_ok = check_tcp_port(db_host, db_port)
    return {"status": "READY" if db_ok else "NOT_READY"}


@router.get("/live")
async def live() -> dict[str, Any]:
    """Liveness endpoint asserting standard FastAPI runner status."""
    return {"status": "ALIVE"}


__all__ = ["router"]
