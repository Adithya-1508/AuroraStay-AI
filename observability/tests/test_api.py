import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app


@pytest.mark.asyncio
async def test_api_agents_observability() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/agents")
    assert res.status_code == 200
    assert len(res.json()) == 2
    assert res.json()[0]["agent_name"] == "GuestConcierge"


@pytest.mark.asyncio
async def test_api_prompts_redaction() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/prompts")
    assert res.status_code == 200
    assert len(res.json()) >= 1
    assert "[REDACTED_EMAIL]" in res.json()[0]["variables_redacted"]


@pytest.mark.asyncio
async def test_api_models_governance() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/models")
    assert res.status_code == 200
    assert len(res.json()) >= 2


@pytest.mark.asyncio
async def test_api_workflows_telemetry() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/workflows")
    assert res.status_code == 200
    assert res.json()[0]["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_api_incidents_management() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/incidents")
    assert res.status_code == 200
    assert len(res.json()) >= 1
    assert res.json()[0]["status"] == "RESOLVED"


@pytest.mark.asyncio
async def test_api_cost_intelligence() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/cost")
    assert res.status_code == 200
    assert res.json()["currency"] == "USD"
    assert res.json()["total_cost"] > 0.0


@pytest.mark.asyncio
async def test_api_drift_detection() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/drift")
    assert res.status_code == 200
    assert "metrics" in res.json()


@pytest.mark.asyncio
async def test_api_evaluation_records() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/observability/evaluation")
    assert res.status_code == 200
    assert len(res.json()) >= 1


@pytest.mark.asyncio
async def test_api_evaluate_triggers() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. RAG Evaluation
        res_rag = await ac.post(
            "/api/v1/observability/evaluate",
            json={
                "evaluation_type": "RAG",
                "predictions": ["deluxe suite is clean"],
                "actuals": ["deluxe suite is clean"],
            },
        )
        assert res_rag.status_code == 200
        assert res_rag.json()["metrics"]["groundedness"] == 1.0

        # 2. MODEL Evaluation
        res_mod = await ac.post(
            "/api/v1/observability/evaluate",
            json={
                "evaluation_type": "MODEL",
                "predictions": [1.1, 2.0],
                "actuals": [1.0, 2.0],
            },
        )
        assert res_mod.status_code == 200
        assert "mean_squared_error" in res_mod.json()["metrics"]

        # 3. PROMPT Evaluation
        res_pr = await ac.post(
            "/api/v1/observability/evaluate",
            json={
                "evaluation_type": "PROMPT",
                "predictions": ["output content"],
                "actuals": ["none"],
            },
        )
        assert res_pr.status_code == 200
        assert "conformity_score" in res_pr.json()["metrics"]

        # 4. Error Path
        res_err = await ac.post(
            "/api/v1/observability/evaluate",
            json={
                "evaluation_type": "INVALID_TYPE",
                "predictions": [],
                "actuals": [],
            },
        )
        assert res_err.status_code == 400


@pytest.mark.asyncio
async def test_api_alert_trigger() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/observability/alerts",
            json={
                "component": "openai_provider",
                "severity": "CRITICAL",
                "message": "Model timeout failures",
            },
        )
    assert res.status_code == 200
    assert res.json()["alert_registered"] is True
