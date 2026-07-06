import hashlib
import time
from typing import Any


class AICache:
    """Caching layer storing prompt hashes and responses with TTL expirations checks."""

    def __init__(self, default_ttl: float = 3600.0) -> None:
        self.default_ttl = default_ttl
        self._store: dict[str, dict[str, Any]] = {}

    def _hash_messages(
        self, messages: list[dict[str, Any]], model: str, provider: str
    ) -> str:
        """Computes a unique SHA-256 hash representing request inputs signature."""
        hasher = hashlib.sha256()
        serialized = f"{str(messages)}:{model}:{provider}".encode()
        hasher.update(serialized)
        return hasher.hexdigest()

    def get(
        self, messages: list[dict[str, Any]], model: str, provider: str
    ) -> Any | None:
        """Retrieves cached response matching inputs signature, checking expiration."""
        key = self._hash_messages(messages, model, provider)
        entry = self._store.get(key)
        if entry is None:
            return None

        if time.time() > entry["expires_at"]:
            del self._store[key]
            return None

        return entry["response"]

    def set(
        self,
        messages: list[dict[str, Any]],
        model: str,
        provider: str,
        response: Any,
        ttl: float | None = None,
    ) -> None:
        """Stores a response linked to key signature with expiration boundaries."""
        key = self._hash_messages(messages, model, provider)
        ttl_val = ttl if ttl is not None else self.default_ttl
        self._store[key] = {
            "response": response,
            "expires_at": time.time() + ttl_val,
            "timestamp": time.time(),
        }

    def clear(self) -> None:
        """Flushes cache."""
        self._store.clear()


__all__ = ["AICache"]
