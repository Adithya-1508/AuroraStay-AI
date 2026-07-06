import json
from typing import Any

from sqlalchemy import text

from backend.agents.checkpoints.base import BaseCheckpointer


class PostgresCheckpointer(BaseCheckpointer):
    """PostgreSQL database checkpoint saver using raw session executions."""

    def __init__(self, session_maker: Any) -> None:
        self.session_maker = session_maker

    async def initialize_table(self) -> None:
        """Initializes database checkpoints table schema if missing."""
        query = """
        CREATE TABLE IF NOT EXISTS agent_checkpoints (
            thread_id VARCHAR(255) NOT NULL,
            checkpoint_id VARCHAR(255) NOT NULL,
            state TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (thread_id, checkpoint_id)
        );
        """
        async with self.session_maker() as session:
            await session.execute(text(query))
            await session.commit()

    async def save(
        self, thread_id: str, checkpoint_id: str, state: dict[str, Any]
    ) -> None:
        """Saves or updates state checkpoint details in database table."""
        state_json = json.dumps(state)
        query = """
        INSERT INTO agent_checkpoints (thread_id, checkpoint_id, state)
        VALUES (:thread_id, :checkpoint_id, :state)
        ON CONFLICT (thread_id, checkpoint_id)
        DO UPDATE SET state = EXCLUDED.state;
        """
        async with self.session_maker() as session:
            await session.execute(
                text(query),
                {
                    "thread_id": thread_id,
                    "checkpoint_id": checkpoint_id,
                    "state": state_json,
                },
            )
            await session.commit()

    async def load(
        self, thread_id: str, checkpoint_id: str | None = None
    ) -> dict[str, Any] | None:
        """Loads and parses checkpoint JSON payload from database records."""
        if checkpoint_id:
            query = """
            SELECT state FROM agent_checkpoints
            WHERE thread_id = :thread_id AND checkpoint_id = :checkpoint_id;
            """
            params = {"thread_id": thread_id, "checkpoint_id": checkpoint_id}
        else:
            query = """
            SELECT state FROM agent_checkpoints
            WHERE thread_id = :thread_id
            ORDER BY created_at DESC, checkpoint_id DESC LIMIT 1;
            """
            params = {"thread_id": thread_id}

        async with self.session_maker() as session:
            res = await session.execute(text(query), params)
            row = res.fetchone()
            if row:
                return json.loads(row[0])  # type: ignore
            return None

    async def list_checkpoints(self, thread_id: str) -> list[dict[str, Any]]:
        """Lists active checkpoint entries stored under thread_id key."""
        query = """
        SELECT checkpoint_id, state FROM agent_checkpoints
        WHERE thread_id = :thread_id
        ORDER BY created_at DESC, checkpoint_id DESC;
        """
        async with self.session_maker() as session:
            res = await session.execute(text(query), {"thread_id": thread_id})
            rows = res.fetchall()
            return [{"checkpoint_id": r[0], "state": json.loads(r[1])} for r in rows]


__all__ = ["PostgresCheckpointer"]
