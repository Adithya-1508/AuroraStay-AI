import time
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from observability.telemetry.logging import get_correlation_id, logger


@contextmanager
def start_trace_span(
    span_name: str, attributes: dict[str, Any] | None = None
) -> Generator[dict[str, Any], None, None]:
    """Context manager simulating an OpenTelemetry span execution trace."""
    start_time = time.time()
    correlation_id = get_correlation_id()
    attrs = attributes or {}

    logger.info(
        "span_started",
        span_name=span_name,
        correlation_id=correlation_id,
        attributes=attrs,
    )

    span_context = {
        "span_name": span_name,
        "correlation_id": correlation_id,
        "attributes": attrs,
    }

    try:
        yield span_context
    except Exception as e:
        logger.error(
            "span_failed",
            span_name=span_name,
            correlation_id=correlation_id,
            error=str(e),
        )
        raise
    finally:
        latency = time.time() - start_time
        logger.info(
            "span_ended",
            span_name=span_name,
            correlation_id=correlation_id,
            duration_sec=latency,
        )
