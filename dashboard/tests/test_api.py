import pytest
from httpx import ASGITransport, AsyncClient

from backend.auth.permissions import get_current_user_context
from backend.main import app
from dashboard.permissions.guard import (
    require_executive,
    require_guest,
    require_operations,
    require_revenue,
)


@pytest.fixture(autouse=True)
def clean_dependency_overrides() -> None:
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_dashboard_layout() -> None:
    # 1. Executive Role
    app.dependency_overrides[get_current_user_context] = lambda: {
        "sub": "exec-1",
        "role": "Executive",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/layout")
    assert res.status_code == 200
    assert res.json()["role"] == "Executive"
    assert res.json()["columns"] == 12

    # 2. Staff Role
    app.dependency_overrides[get_current_user_context] = lambda: {
        "sub": "staff-1",
        "role": "Housekeeper",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/layout")
    assert res.status_code == 200
    assert res.json()["role"] == "Housekeeper"
    assert len(res.json()["widgets"]) == 2


@pytest.mark.asyncio
async def test_get_executive_overview() -> None:
    app.dependency_overrides[require_executive] = lambda: {
        "sub": "exec-1",
        "role": "Executive",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/executive")
    assert res.status_code == 200
    data = res.json()
    assert "business_health_score" in data
    assert "metrics" in data
    assert "widgets" in data
    assert len(data["widgets"]) > 0


@pytest.mark.asyncio
async def test_get_revenue_dashboard() -> None:
    app.dependency_overrides[require_revenue] = lambda: {
        "sub": "rev-1",
        "role": "Revenue Manager",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/revenue")
    assert res.status_code == 200
    data = res.json()
    assert data["filters_applied"]["department"] == "Revenue"
    assert "kpis" in data


@pytest.mark.asyncio
async def test_get_operations_dashboard() -> None:
    app.dependency_overrides[require_operations] = lambda: {
        "sub": "ops-1",
        "role": "Operations Manager",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/operations")
    assert res.status_code == 200
    data = res.json()
    assert data["filters_applied"]["department"] == "housekeeping"
    assert "kpis" in data


@pytest.mark.asyncio
async def test_get_guests_dashboard() -> None:
    app.dependency_overrides[require_guest] = lambda: {
        "sub": "gst-1",
        "role": "Guest Experience Manager",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/guests")
    assert res.status_code == 200
    data = res.json()
    assert data["filters_applied"]["guest_segment"] == "leisure"


@pytest.mark.asyncio
async def test_get_active_alerts() -> None:
    app.dependency_overrides[require_operations] = lambda: {
        "sub": "ops-1",
        "role": "Operations Manager",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/alerts")
    assert res.status_code == 200
    alerts = res.json()
    assert len(alerts) > 0
    assert any(a["title"] == "Low Forecasted Occupancy" for a in alerts)


@pytest.mark.asyncio
async def test_get_occupancy_forecasts() -> None:
    app.dependency_overrides[require_revenue] = lambda: {
        "sub": "rev-1",
        "role": "Revenue Manager",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get(
            "/api/v1/dashboard/forecasts?horizon_days=10&compare_historical=true"
        )
    assert res.status_code == 200
    data = res.json()
    assert data["horizon_days"] == 10
    assert len(data["data_points"]) == 10


@pytest.mark.asyncio
async def test_list_previous_reports() -> None:
    app.dependency_overrides[require_executive] = lambda: {
        "sub": "exec-1",
        "role": "Executive",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/reports")
    assert res.status_code == 200
    assert len(res.json()) >= 1


@pytest.mark.asyncio
async def test_generate_ai_report() -> None:
    app.dependency_overrides[require_executive] = lambda: {
        "sub": "exec-1",
        "role": "Executive",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/dashboard/reports/generate",
            json={"interval": "DAILY", "department": "REVENUE", "custom_notes": "None"},
        )
    assert res.status_code == 200
    data = res.json()
    assert data["interval"] == "DAILY"
    assert "ai_insights" in data


@pytest.mark.asyncio
async def test_get_decision_intelligence_records() -> None:
    app.dependency_overrides[require_revenue] = lambda: {
        "sub": "rev-1",
        "role": "Revenue Manager",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/dashboard/decisions")
    assert res.status_code == 200
    assert len(res.json()) >= 1


@pytest.mark.asyncio
async def test_query_executive_assistant() -> None:
    app.dependency_overrides[require_executive] = lambda: {
        "sub": "exec-1",
        "role": "Executive",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/dashboard/assistant",
            json={"query": "Why is SLA low?"},
        )
    assert res.status_code == 200
    assert "response" in res.json()
    assert len(res.json()["suggested_actions"]) > 0


@pytest.mark.asyncio
async def test_export_dashboard_dataset() -> None:
    app.dependency_overrides[require_executive] = lambda: {
        "sub": "exec-1",
        "role": "Executive",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/dashboard/exports",
            json={"export_format": "CSV", "dataset_type": "EXECUTIVE", "filters": {}},
        )
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert b"Metric,Value,Status" in res.content


@pytest.mark.asyncio
async def test_explain_chart_visuals() -> None:
    app.dependency_overrides[require_executive] = lambda: {
        "sub": "exec-1",
        "role": "Executive",
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/dashboard/visual-analytics/explain",
            json={
                "chart_type": "LINE_CHART",
                "metric_name": "Revenue",
                "historical_data": [100.0, 105.0],
                "forecast_data": [110.0, 115.0],
            },
        )
    assert res.status_code == 200
    data = res.json()
    assert "Revenue is projected to be increased" in data["status"]
    assert len(data["causes"]) > 0
