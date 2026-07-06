import asyncio
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseTool(ABC):
    """Abstract base class representing an executable LLM tool."""

    name: str
    description: str
    args_schema: type[BaseModel]
    permissions: list[str] = []
    timeout_sec: float = 30.0
    retries: int = 0

    @abstractmethod
    async def _run(self, **kwargs: Any) -> Any:
        """Internal execution body logic defined by subclass implementations."""
        pass

    async def execute(self, **kwargs: Any) -> Any:
        """Executes the tool with validation, retries, and timeout constraints."""
        validated = self.args_schema.model_validate(kwargs)

        attempt = 0
        while attempt <= self.retries:
            try:
                return await asyncio.wait_for(
                    self._run(**validated.model_dump()),
                    timeout=self.timeout_sec,
                )
            except Exception as e:
                attempt += 1
                if attempt > self.retries:
                    raise e


class ToolExecutor:
    """Orchestrator managing tools registrations and runtime executions checks."""

    def __init__(self, tools: list[BaseTool] | None = None) -> None:
        self._tools: dict[str, BaseTool] = {}
        if tools:
            for t in tools:
                self.register(t)

    def register(self, tool: BaseTool) -> None:
        """Adds an executable tool instance to registration index."""
        self._tools[tool.name.strip()] = tool

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        caller_permissions: list[str] | None = None,
    ) -> Any:
        """Checks caller scope permissions and executes registered tool by name."""
        tool = self._tools.get(tool_name.strip())
        if not tool:
            raise KeyError(f"Tool '{tool_name}' not registered in executor.")

        # Enforce scope checks if tool specifies permissions
        if tool.permissions:
            caller_perms = caller_permissions or []
            for perm in tool.permissions:
                if perm not in caller_perms:
                    raise PermissionError(
                        f"Lacking required permission '{perm}' "
                        f"to invoke tool '{tool_name}'."
                    )

        return await tool.execute(**arguments)


__all__ = ["BaseTool", "ToolExecutor"]
