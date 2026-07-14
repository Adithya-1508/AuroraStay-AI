import hashlib
import secrets
from typing import Any


class APIKeyManager:
    """Generates, hashes, and validates API keys for service accounts and agents."""

    def __init__(self) -> None:
        # Maps hashed API key -> identity metadata dict
        self._key_registry: dict[str, dict[str, Any]] = {}

    def _hash_key(self, api_key: str) -> str:
        return hashlib.sha256(api_key.encode()).hexdigest()

    def generate_api_key(self, identity_id: str, department: str, name: str) -> str:
        """Creates a cryptographically secure key and registers it."""
        raw_key = f"hk_{secrets.token_urlsafe(32)}"
        hashed = self._hash_key(raw_key)
        self._key_registry[hashed] = {
            "identity_id": identity_id,
            "department": department,
            "name": name,
            "created_at": hash(raw_key),  # simple indicator for metadata tests
        }
        return raw_key

    def validate_api_key(self, api_key: str) -> dict[str, Any] | None:
        """Verifies if raw API key exists and returns identity info."""
        hashed = self._hash_key(api_key)
        return self._key_registry.get(hashed)

    def revoke_api_key(self, api_key: str) -> bool:
        """Revokes API key."""
        hashed = self._hash_key(api_key)
        if hashed in self._key_registry:
            del self._key_registry[hashed]
            return True
        return False
