from abc import ABC, abstractmethod
from typing import Any


class BaseCheckpointer(ABC):
    """Abstract base class for saving and restoring agent state checkpoints."""

    @abstractmethod
    async def save(
        self, thread_id: str, checkpoint_id: str, state: dict[str, Any]
    ) -> None:
        """Saves a state checkpoint snapshot under a target thread_id."""
        pass

    @abstractmethod
    async def load(
        self, thread_id: str, checkpoint_id: str | None = None
    ) -> dict[str, Any] | None:
        """Loads and returns a checkpoint state snapshot by thread and ID."""
        pass

    @abstractmethod
    async def list_checkpoints(self, thread_id: str) -> list[dict[str, Any]]:
        """Lists metadata of all checkpoints recorded for a target thread."""
        pass


__all__ = ["BaseCheckpointer"]
