from collections.abc import Callable, Sequence
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from backend.auth.jwt import decode_access_token
from shared.exceptions import AuthenticationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token", auto_error=False)


def get_current_user_context(
    token: str | None = Depends(oauth2_scheme),
) -> dict[str, Any]:
    """Extracts and verifies JWT token payload to establish current user context."""
    if not token:
        raise AuthenticationError("Authorization token is missing.")
    return decode_access_token(token)


def require_role(
    allowed_roles: Sequence[str],
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """Ensures the current user has one of the allowed roles."""

    def dependency(
        current_user: dict[str, Any] = Depends(get_current_user_context),
    ) -> dict[str, Any]:
        user_role = current_user.get("role")
        if not user_role or user_role not in allowed_roles:
            raise AuthenticationError(
                f"Access denied. User role '{user_role}' lacks permissions."
            )
        return current_user

    return dependency


__all__ = ["oauth2_scheme", "get_current_user_context", "require_role"]
