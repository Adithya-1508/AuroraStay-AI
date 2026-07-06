import time
import uuid
from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, Request, Response

from backend.core.logging import logger


def register_middleware(app: FastAPI) -> None:
    """Registers timing, request ID, and logs on the application."""

    @app.middleware("http")
    async def correlation_id_and_timing_middleware(
        request: Request, call_next: Callable[..., Any]
    ) -> Response:
        # Extract or generate Request ID
        req_id = request.headers.get("X-Request-ID")
        if not req_id:
            req_id = f"req_{uuid.uuid4()}"
        request.state.request_id = req_id

        # Measure timing
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        latency_ms = (time.perf_counter() - start_time) * 1000.0

        # Inject headers
        response.headers["X-Response-Time"] = f"{latency_ms:.2f}ms"
        response.headers["X-Request-ID"] = req_id

        # Log details
        logger.info(
            "HTTP Request Processed",
            request_id=req_id,
            http_method=request.method,
            http_path=request.url.path,
            status_code=response.status_code,
            latency_ms=round(latency_ms, 2),
        )

        return response


__all__ = ["register_middleware"]
