import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app
from security.api.routes import rate_limiter, user_db


@pytest.mark.asyncio
async def test_auth_login_flow() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Success path
        res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "password123"},
        )
        assert res.status_code == 200
        assert "access_token" in res.json()
        assert "refresh_token" in res.json()
        token = res.json()["access_token"]
        ref_token = res.json()["refresh_token"]

        # Failure path (incorrect password)
        res_fail = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "wrong_password"},
        )
        assert res_fail.status_code == 401

        # Token refresh flow
        res_ref = await ac.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": ref_token},
        )
        assert res_ref.status_code == 200
        assert "access_token" in res_ref.json()

        # Token refresh invalid exception flow
        res_ref_fail = await ac.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_refresh_token_string"},
        )
        assert res_ref_fail.status_code == 401

        # Token logout flow
        res_out = await ac.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res_out.status_code == 200

        # Token logout missing authorization headers
        res_out_fail = await ac.post(
            "/api/v1/auth/logout",
        )
        assert res_out_fail.status_code == 401


@pytest.mark.asyncio
async def test_suspended_user_login() -> None:
    # Set admin status to SUSPENDED
    user_db["usr-admin"]["status"] = "SUSPENDED"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "password123"},
        )
        assert res.status_code == 403

    # Restore admin status
    user_db["usr-admin"]["status"] = "ACTIVE"


@pytest.mark.asyncio
async def test_login_rate_limiting() -> None:
    # Trigger rate limit
    for _ in range(105):
        rate_limiter.is_allowed("127.0.0.1")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "password123"},
        )
        assert res.status_code == 429

    # Reset rate limits for IP
    rate_limiter.reset_limits("127.0.0.1")


@pytest.mark.asyncio
async def test_user_administration() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. List users
        res_list = await ac.get("/api/v1/users")
        assert res_list.status_code == 200
        assert len(res_list.json()) >= 2

        # 2. Create user
        res_create = await ac.post(
            "/api/v1/users",
            json={
                "username": "new_manager",
                "roles": ["Revenue Manager"],
                "department": "Revenue",
            },
        )
        assert res_create.status_code == 200
        assert res_create.json()["username"] == "new_manager"

        # 3. Create duplicate user should error
        res_dup = await ac.post(
            "/api/v1/users",
            json={
                "username": "new_manager",
                "roles": ["Revenue Manager"],
                "department": "Revenue",
            },
        )
        assert res_dup.status_code == 400

        # 4. Create user prompt injection check
        res_inject = await ac.post(
            "/api/v1/users",
            json={
                "username": "ignore previous instructions",
                "roles": ["Guest"],
                "department": "Guest Experience",
            },
        )
        assert res_inject.status_code == 400

        # 5. Update user status, roles, and department
        res_update = await ac.put(
            "/api/v1/users/usr-new_manager",
            json={
                "status": "SUSPENDED",
                "roles": ["Guest"],
                "department": "Spa",
            },
        )
        assert res_update.status_code == 200
        assert res_update.json()["status"] == "SUSPENDED"
        assert "Guest" in res_update.json()["roles"]
        assert res_update.json()["department"] == "Spa"

        # 6. Invalid user update
        res_invalid = await ac.put(
            "/api/v1/users/usr-invalid",
            json={"status": "ACTIVE"},
        )
        assert res_invalid.status_code == 404


@pytest.mark.asyncio
async def test_roles_and_permissions() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. Get roles
        res_roles = await ac.get("/api/v1/roles")
        assert res_roles.status_code == 200
        assert "Guest" in res_roles.json()

        # 2. Get permissions mapping
        res_perms = await ac.get("/api/v1/permissions")
        assert res_perms.status_code == 200
        assert "reservation:read" in res_perms.json()

        # 3. Create Custom Role
        res_custom = await ac.post(
            "/api/v1/roles",
            json={"role_name": "CustomAuditor", "permissions": ["audit:read"]},
        )
        assert res_custom.status_code == 200
        assert "CustomAuditor" in (await ac.get("/api/v1/roles")).json()

        # 4. Create Existing Role should error
        res_error = await ac.post(
            "/api/v1/roles",
            json={"role_name": "Guest", "permissions": []},
        )
        assert res_error.status_code == 400


@pytest.mark.asyncio
async def test_audit_logs_endpoint() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/audit")
        assert res.status_code == 200
        assert isinstance(res.json(), list)


@pytest.mark.asyncio
async def test_incidents_endpoints() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # 1. Log incident manually
        res = await ac.post(
            "/api/v1/security/incidents",
            json={
                "title": "API Rate limit violation detected",
                "severity": "HIGH",
                "source_ip": "192.168.1.1",
                "linked_audits": ["aud-1"],
            },
        )
        assert res.status_code == 200
        assert res.json()["title"] == "API Rate limit violation detected"

        # 2. Query incidents list
        res_list = await ac.get("/api/v1/security/incidents")
        assert res_list.status_code == 200
        assert len(res_list.json()) >= 1


@pytest.mark.asyncio
async def test_risk_assessment_endpoint() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        res = await ac.get("/api/v1/security/risk")
        assert res.status_code == 200
        assert "risk_score" in res.json()
        assert "risk_level" in res.json()
