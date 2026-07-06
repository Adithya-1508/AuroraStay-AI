from typing import Any

from backend.agents.core.base_agent import BaseAgent


class AgentRegistry:
    """Registry maintaining metadata and class definitions for active agents."""

    def __init__(self) -> None:
        self._agents: dict[str, type[BaseAgent]] = {}

    def register(self, agent_cls: type[BaseAgent]) -> None:
        """Registers a BaseAgent class configuration into index."""
        name = agent_cls.name.strip()
        self._agents[name] = agent_cls

    def get(self, name: str) -> type[BaseAgent]:
        """Retrieves registered agent class by unique name."""
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not found in registry.")
        return self._agents[name]

    def list_agents(self) -> list[dict[str, Any]]:
        """Compiles active agents metadata properties registry listing."""
        return [
            {
                "name": cls.name,
                "version": cls.version,
                "description": cls.description,
                "owner": cls.owner,
                "capabilities": cls.capabilities,
                "required_tools": cls.required_tools,
                "supported_workflows": cls.supported_workflows,
                "status": cls.status,
            }
            for cls in self._agents.values()
        ]


__all__ = ["AgentRegistry"]
