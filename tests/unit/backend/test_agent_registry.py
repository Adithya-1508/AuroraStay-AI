import pytest

from backend.agents.core.base_agent import (
    BaseAgent,
    ExecutionPlan,
    ExecutionResult,
)
from backend.agents.core.factory import AgentFactory
from backend.agents.core.registry import AgentRegistry


class DummyAgent(BaseAgent):
    name = "dummy-agent"
    version = "1.0.0"
    description = "A dummy agent for testing."
    owner = "infrastructure"

    async def _on_plan(self, goal: str) -> ExecutionPlan:
        return ExecutionPlan(plan_id="plan-1")

    async def _on_execute(self, plan: ExecutionPlan) -> ExecutionResult:
        return ExecutionResult(plan_id="plan-1", success=True)


def test_agent_registry_registration() -> None:
    """Verifies that agents can be registered, listed, and instantiated."""
    registry = AgentRegistry()
    assert len(registry.list_agents()) == 0

    registry.register(DummyAgent)
    assert len(registry.list_agents()) == 1

    metadata = registry.list_agents()[0]
    assert metadata["name"] == "dummy-agent"
    assert metadata["version"] == "1.0.0"

    factory = AgentFactory(registry)
    agent = factory.create("dummy-agent")
    assert isinstance(agent, DummyAgent)
    assert agent.state == "UNINITIALIZED"


def test_agent_registry_missing_error() -> None:
    """Verifies registry raises KeyError on requesting unregistered agent name."""
    registry = AgentRegistry()
    with pytest.raises(KeyError, match="not found in registry"):
        registry.get("invalid-agent")
