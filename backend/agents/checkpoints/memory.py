from typing import Any

from backend.agents.checkpoints.base import BaseCheckpointer


class MemoryCheckpointer(BaseCheckpointer):
    """In-memory checkpoint saver for unit testing and local executions."""

    def __init__(self) -> None:
        # thread_id -> {checkpoint_id: state_dict}
        self._storage: dict[str, dict[str, dict[str, Any]]] = {}

    async def save(
        self, thread_id: str, checkpoint_id: str, state: dict[str, Any]
    ) -> None:
        """Saves a shallow copy of the state checkpoint."""
        if thread_id not in self._storage:
            self._storage[thread_id] = {}
        self._storage[thread_id][checkpoint_id] = dict(state)

    async def load(
        self, thread_id: str, checkpoint_id: str | None = None
    ) -> dict[str, Any] | None:
        """Loads and retrieves state snapshot by target parameters."""
        if thread_id not in self._storage:
            return None
        thread_runs = self._storage[thread_id]
        if not thread_runs:
            return None
        if checkpoint_id:
            return thread_runs.get(checkpoint_id)

        # Fallback returning the latest saved checkpoint version
        latest_id = list(thread_runs.keys())[-1]
        return thread_runs[latest_id]

    async def list_checkpoints(self, thread_id: str) -> list[dict[str, Any]]:
        """Compiles metadata dict for all checkpoints under thread_id."""
        if thread_id not in self._storage:
            return []
        return [
            {"checkpoint_id": cid, "state": state}
            for cid, state in self._storage[thread_id].items()
        ]


__all__ = ["MemoryCheckpointer"]
