import jwt
import pytest

from security.authentication.jwt import JWTAuth
from security.authentication.keys import APIKeyManager


def test_jwt_auth_lifecycle() -> None:
    # 1. Access token
    token = JWTAuth.create_access_token("usr-1", "USER", ["Guest"], "Reception")
    payload = JWTAuth.decode_token(token)
    assert payload["sub"] == "usr-1"
    assert payload["type"] == "USER"
    assert "Guest" in payload["roles"]
    assert payload["department"] == "Reception"

    # 2. Refresh token
    ref_token = JWTAuth.create_refresh_token("usr-1")
    ref_payload = JWTAuth.decode_token(ref_token)
    assert ref_payload["sub"] == "usr-1"

    # 3. Revocation
    JWTAuth.revoke_token(token)
    with pytest.raises(jwt.InvalidTokenError):
        JWTAuth.decode_token(token)

    # 4. Invalid signatures
    with pytest.raises(jwt.InvalidTokenError):
        JWTAuth.decode_token("invalid_token_header.body.signature")

    # 5. Expired token signatures
    from datetime import UTC, datetime, timedelta

    from security.authentication.jwt import JWT_ALGORITHM, JWT_SECRET

    expire = datetime.now(UTC) - timedelta(minutes=10)
    payload = {
        "sub": "usr-1",
        "exp": expire,
        "iat": datetime.now(UTC),
    }
    expired_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    with pytest.raises(jwt.ExpiredSignatureError):
        JWTAuth.decode_token(expired_token)


def test_api_keys_verification() -> None:
    mgr = APIKeyManager()

    # Generate key
    key = mgr.generate_api_key("agent-1", "Revenue", "RevenueAgent")
    assert key.startswith("hk_")

    # Validate key
    meta = mgr.validate_api_key(key)
    assert meta is not None
    assert meta["identity_id"] == "agent-1"
    assert meta["department"] == "Revenue"

    # Revoke key
    assert mgr.revoke_api_key(key) is True
    assert mgr.validate_api_key(key) is None
    assert mgr.revoke_api_key(key) is False


def test_identity_model_instantiation() -> None:
    from security.identity.models import Identity, IdentityStatus, IdentityType

    identity = Identity(
        identity_id="usr-test",
        type=IdentityType.USER,
        name="Test User",
        owner="admin",
        status=IdentityStatus.ACTIVE,
        assigned_roles=["Guest"],
        department="Reception",
    )
    assert identity.identity_id == "usr-test"
    assert identity.type == IdentityType.USER
    assert identity.status == IdentityStatus.ACTIVE
    assert identity.assigned_roles == ["Guest"]
