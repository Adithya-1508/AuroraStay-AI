from datetime import UTC, datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.core.logging import logger
from shared.exceptions import (
    AuthenticationError,
    BusinessRuleError,
    EntityNotFoundError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Registers exception handlers translating domain errors to HTTP."""

    @app.exception_handler(AuthenticationError)
    async def auth_exception_handler(
        request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        req_id = getattr(request.state, "request_id", "")
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": {"code": "UNAUTHENTICATED", "message": exc.message},
                "request_id": req_id,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @app.exception_handler(EntityNotFoundError)
    async def not_found_exception_handler(
        request: Request, exc: EntityNotFoundError
    ) -> JSONResponse:
        req_id = getattr(request.state, "request_id", "")
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {"code": "NOT_FOUND", "message": exc.message},
                "request_id": req_id,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @app.exception_handler(BusinessRuleError)
    async def business_exception_handler(
        request: Request, exc: BusinessRuleError
    ) -> JSONResponse:
        req_id = getattr(request.state, "request_id", "")
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": {"code": "BUSINESS_VIOLATION", "message": exc.message},
                "request_id": req_id,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        req_id = getattr(request.state, "request_id", "")
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {"code": "VALIDATION_ERROR", "message": str(exc.errors())},
                "request_id": req_id,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        req_id = getattr(request.state, "request_id", "")
        logger.exception("Unhandle exception", request_id=req_id, error=str(exc))
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected system error occurred.",
                },
                "request_id": req_id,
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
