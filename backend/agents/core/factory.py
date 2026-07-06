from backend.agents.core.base_agent import BaseAgent
from backend.agents.core.registry import AgentRegistry


class AgentFactory:
    """Factory instantiating registered agents dynamically from registry records."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def create(self, name: str) -> BaseAgent:
        """Instantiates and returns an agent class instance."""
        agent_cls = self.registry.get(name)
        return agent_cls()


__all__ = ["AgentFactory"]
