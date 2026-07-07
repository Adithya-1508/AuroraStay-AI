from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, Request

from backend.auth.permissions import get_current_user_context
from business.guest.api.routes import router as guests_router
from business.ops.api.routes import router as ops_router
from business.reservation.api.routes import router as reservations_router

router = APIRouter()

router.include_router(
    reservations_router, prefix="/reservations", tags=["Reservations"]
)
router.include_router(guests_router, tags=["Guests"])
router.include_router(ops_router, tags=["Operations"])


@router.get("/ping")
async def ping(request: Request) -> dict[str, Any]:
    """Public heartbeat check route verifying routing namespace."""
    req_id = getattr(request.state, "request_id", "")
    return {
        "success": True,
        "data": {"message": "pong"},
        "metadata": {},
        "request_id": req_id,
        "timestamp": datetime.now(UTC).isoformat(),
    }


@router.get("/protected")
async def protected(
    request: Request, user: dict[str, Any] = Depends(get_current_user_context)
) -> dict[str, Any]:
    """Authenticated heartbeat check route verifying security token parsing."""
    req_id = getattr(request.state, "request_id", "")
    return {
        "success": True,
        "data": {
            "message": f"Access granted for sub: {user.get('sub')}",
            "role": user.get("role"),
        },
        "metadata": {},
        "request_id": req_id,
        "timestamp": datetime.now(UTC).isoformat(),
    }


__all__ = ["router"]
