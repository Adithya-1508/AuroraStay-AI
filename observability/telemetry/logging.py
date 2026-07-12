import contextvars
import uuid
from collections.abc import Mapping, MutableMapping
from typing import Any

import structlog

# Global correlation ID contextvar
correlation_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "correlation_id", default=""
)


def get_correlation_id() -> str:
    """Retrieves the current request context correlation ID."""
    cid = correlation_id_ctx.get()
    if not cid:
        cid = str(uuid.uuid4())
        correlation_id_ctx.set(cid)
    return cid


def set_correlation_id(cid: str) -> None:
    """Sets a new correlation ID for the active request context."""
    correlation_id_ctx.set(cid)


def add_correlation_id_processor(
    logger: Any, method_name: str, event_dict: MutableMapping[str, Any]
) -> Mapping[str, Any]:
    """Structlog processor injecting correlation ID into log context."""
    event_dict["correlation_id"] = get_correlation_id()
    return event_dict


# Configures structlog with standard JSON and correlation injection
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        add_correlation_id_processor,
        structlog.processors.JSONRenderer(),
    ]
)

logger = structlog.get_logger("observability")
