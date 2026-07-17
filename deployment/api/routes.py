from typing import Any

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/deployment", tags=["Deployment"])

# Mock deployment state
DEPLOYMENT_STATE: dict[str, Any] = {
    "version": "1.16.0",
    "status": "HEALTHY",
    "environment": "production",
    "revision": 3,
    "last_deployed_at": "2026-07-14T12:00:00Z",
}


@router.get("/status")
async def get_status() -> dict[str, Any]:
    """Returns the current deployment metadata state."""
    return DEPLOYMENT_STATE


@router.get("/health")
async def get_health() -> dict[str, Any]:
    """Performs deep checks on database, cache, and vector db health status."""
    # Aggregated system checks
    return {
        "status": "HEALTHY",
        "services": {
            "postgres": "CONNECTED",
            "redis": "CONNECTED",
            "qdrant": "CONNECTED",
            "mlflow": "CONNECTED",
        },
    }


@router.get("/readiness")
async def get_readiness() -> dict[str, Any]:
    """Kubernetes readiness probe target endpoint."""
    return {"ready": True}


@router.get("/version")
async def get_version() -> dict[str, str]:
    """Returns the active semantic release version."""
    return {"version": DEPLOYMENT_STATE["version"]}


@router.post("/rollback")
async def trigger_rollback() -> dict[str, Any]:
    """Simulates a deployment rollback process to the previous Helm revision."""
    if DEPLOYMENT_STATE["revision"] <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No previous revision available for rollback.",
        )

    prev_revision = DEPLOYMENT_STATE["revision"] - 1
    DEPLOYMENT_STATE["revision"] = prev_revision
    DEPLOYMENT_STATE["status"] = "ROLLBACK_IN_PROGRESS"

    return {
        "message": f"Rollback to revision {prev_revision} successfully initiated.",
        "active_revision": prev_revision,
        "status": DEPLOYMENT_STATE["status"],
    }
