import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app
from deployment.api.routes import DEPLOYMENT_STATE


@pytest.mark.asyncio
async def test_deployment_status_endpoints() -> None:
    # Restore defaults
    DEPLOYMENT_STATE["revision"] = 3
    DEPLOYMENT_STATE["status"] = "HEALTHY"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. Status query
        res_status = await ac.get("/api/v1/deployment/status")
        assert res_status.status_code == 200
        assert res_status.json()["version"] == "1.16.0"

        # 2. Health checks
        res_health = await ac.get("/api/v1/deployment/health")
        assert res_health.status_code == 200
        assert res_health.json()["status"] == "HEALTHY"

        # 3. Readiness checks
        res_ready = await ac.get("/api/v1/deployment/readiness")
        assert res_ready.status_code == 200
        assert res_ready.json()["ready"] is True

        # 4. Version checks
        res_ver = await ac.get("/api/v1/deployment/version")
        assert res_ver.status_code == 200
        assert res_ver.json()["version"] == "1.16.0"


@pytest.mark.asyncio
async def test_deployment_rollback_endpoint() -> None:
    DEPLOYMENT_STATE["revision"] = 3
    DEPLOYMENT_STATE["status"] = "HEALTHY"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Rollback success
        res = await ac.post("/api/v1/deployment/rollback")
        assert res.status_code == 200
        assert res.json()["active_revision"] == 2
        assert res.json()["status"] == "ROLLBACK_IN_PROGRESS"

        # Rollback again to revision 1
        res2 = await ac.post("/api/v1/deployment/rollback")
        assert res2.status_code == 200
        assert res2.json()["active_revision"] == 1

        # Error case: rollback from revision 1 (no previous revision)
        res_fail = await ac.post("/api/v1/deployment/rollback")
        assert res_fail.status_code == 400
