from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_check() -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "details" in data
    assert "database" in data["details"]
    assert "redis" in data["details"]
    assert "qdrant" in data["details"]


def test_ready_check() -> None:
    resp = client.get("/ready")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data


def test_live_check() -> None:
    resp = client.get("/live")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ALIVE"
