from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.exceptions.handlers import register_exception_handlers
from shared.exceptions import (
    AuthenticationError,
    BusinessRuleError,
    EntityNotFoundError,
)

# Instantiate dummy test app
test_app = FastAPI()
register_exception_handlers(test_app)


@test_app.get("/test-auth")
def route_auth() -> None:
    raise AuthenticationError("Custom auth error")


@test_app.get("/test-notfound")
def route_notfound() -> None:
    raise EntityNotFoundError("Custom resource not found")


@test_app.get("/test-business")
def route_business() -> None:
    raise BusinessRuleError("Custom business violation")


@test_app.get("/test-generic")
def route_generic() -> None:
    raise ValueError("Custom generic error")


client = TestClient(test_app, raise_server_exceptions=False)


def test_auth_exception_handler() -> None:
    resp = client.get("/test-auth")
    assert resp.status_code == 401
    data = resp.json()
    assert data["success"] is False
    assert data["error"]["code"] == "UNAUTHENTICATED"
    assert "Custom auth" in data["error"]["message"]


def test_notfound_exception_handler() -> None:
    resp = client.get("/test-notfound")
    assert resp.status_code == 404
    data = resp.json()
    assert data["success"] is False
    assert data["error"]["code"] == "NOT_FOUND"


def test_business_exception_handler() -> None:
    resp = client.get("/test-business")
    assert resp.status_code == 400
    data = resp.json()
    assert data["success"] is False
    assert data["error"]["code"] == "BUSINESS_VIOLATION"


def test_generic_exception_handler() -> None:
    resp = client.get("/test-generic")
    assert resp.status_code == 500
    data = resp.json()
    assert data["success"] is False
    assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
