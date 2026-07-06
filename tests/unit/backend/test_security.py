from datetime import timedelta

import pytest

from backend.auth.jwt import create_access_token, decode_access_token
from backend.auth.password import hash_password, verify_password
from shared.exceptions import AuthenticationError


def test_password_hashing() -> None:
    pwd = "mysecurepassword"  # noqa: S105
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_token_flow() -> None:
    subject = "user_123"
    role = "Staff"
    token = create_access_token(subject, role)
    assert token is not None

    payload = decode_access_token(token)
    assert payload["sub"] == subject
    assert payload["role"] == role


def test_jwt_invalid_token() -> None:
    with pytest.raises(AuthenticationError):
        decode_access_token("invalid.token.payload")


def test_jwt_expired_token() -> None:
    token = create_access_token(
        "user_expired", "Guest", expires_delta=timedelta(seconds=-10)
    )
    with pytest.raises(AuthenticationError) as exc:
        decode_access_token(token)
    assert "expired" in str(exc.value).lower()
