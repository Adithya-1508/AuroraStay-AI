from abc import ABC, abstractmethod
from typing import Any


class BaseMemory(ABC):
    """Abstract base class defining unified memory actions."""

    @abstractmethod
    def store(self, key: str, value: Any) -> None:
        """Stores a value associated with key identifier."""
        pass

    @abstractmethod
    def retrieve(self, key: str) -> Any:
        """Retrieves value corresponding to key identifier."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clears all stored variables inside memory state."""
        pass


class SessionMemory(BaseMemory):
    """Memory persisting transient state variables in a local dict."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def store(self, key: str, value: Any) -> None:
        self._store[key] = value

    def retrieve(self, key: str) -> Any:
        return self._store.get(key)

    def clear(self) -> None:
        self._store.clear()


class ConversationMemory(BaseMemory):
    """Memory appending conversational events in chronological sequence."""

    def __init__(self) -> None:
        self._history: list[dict[str, Any]] = []

    def store(self, key: str, value: Any) -> None:
        self._history.append({"key": key, "value": value})

    def retrieve(self, key: str) -> Any:
        return [item["value"] for item in self._history if item["key"] == key]

    def clear(self) -> None:
        self._history.clear()


class WorkingMemory(BaseMemory):
    """Memory containing working context and planner goals."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def store(self, key: str, value: Any) -> None:
        self._store[key] = value

    def retrieve(self, key: str) -> Any:
        return self._store.get(key)

    def clear(self) -> None:
        self._store.clear()


class LongTermMemory(BaseMemory):
    """Placeholder memory structure for future vector-indexed retrieval systems."""

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}

    def store(self, key: str, value: Any) -> None:
        self._store[key] = value

    def retrieve(self, key: str) -> Any:
        return self._store.get(key)

    def clear(self) -> None:
        self._store.clear()


__all__ = [
    "BaseMemory",
    "SessionMemory",
    "ConversationMemory",
    "WorkingMemory",
    "LongTermMemory",
]
