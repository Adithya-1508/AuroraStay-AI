from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

# Constants
JWT_SECRET = "hospitality_ai_super_secret_key_12345"  # noqa: S105
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Session revocation register (token blacklists)
revoked_tokens: set[str] = set()


class JWTAuth:
    """Manages the lifecycle, encoding, validation, and revocation of JSON Web Tokens."""

    @staticmethod
    def create_access_token(
        identity_id: str, type: str, roles: list[str], department: str
    ) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": identity_id,
            "type": type,
            "roles": roles,
            "department": department,
            "exp": expire,
            "iat": datetime.now(UTC),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(identity_id: str) -> str:
        expire = datetime.now(UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": identity_id,
            "exp": expire,
            "iat": datetime.now(UTC),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        """Decodes JWT payload and verifies expiration."""
        if token in revoked_tokens:
            raise jwt.InvalidTokenError("Token has been revoked")
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError as e:
            raise jwt.ExpiredSignatureError("Token has expired") from e
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError("Invalid token signature") from e

    @staticmethod
    def revoke_token(token: str) -> None:
        """Revokes a token immediately by adding it to the blacklist."""
        revoked_tokens.add(token)
