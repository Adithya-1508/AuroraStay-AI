from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from backend.core.settings import settings
from shared.exceptions import AuthenticationError

ALGORITHM = "HS256"


def create_access_token(
    subject: str, role: str, expires_delta: timedelta | None = None
) -> str:
    """Generates a signed JWT access token containing subject and role claims."""
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)

    to_encode = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(UTC),
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """Decodes and validates a JWT token signature, returning claims if successful."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as err:
        raise AuthenticationError("Token has expired.") from err
    except jwt.InvalidTokenError as err:
        raise AuthenticationError("Invalid token signature.") from err


__all__ = ["create_access_token", "decode_access_token"]
