from fastapi.testclient import TestClient

from backend.auth.jwt import create_access_token
from backend.main import app

client = TestClient(app)


def test_ping_unauthenticated() -> None:
    resp = client.get("/api/v1/ping")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["data"]["message"] == "pong"
    assert "request_id" in data
    assert resp.headers.get("X-Request-ID") == data["request_id"]
    assert resp.headers.get("X-Response-Time") is not None


def test_protected_unauthenticated() -> None:
    resp = client.get("/api/v1/protected")
    assert resp.status_code == 401
    data = resp.json()
    assert data["success"] is False
    assert data["error"]["code"] == "UNAUTHENTICATED"


def test_protected_authenticated() -> None:
    token = create_access_token("guest_user", "Guest")
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/v1/protected", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "guest_user" in data["data"]["message"]
    assert data["data"]["role"] == "Guest"
