import pytest

from backend.agents.core.base_agent import (
    BaseAgent,
    ExecutionPlan,
    ExecutionResult,
)
from backend.agents.core.supervisor import AgentSupervisor


class RecoverableAgent(BaseAgent):
    name = "recoverable-agent"
    version = "1.0.0"
    description = "Agent that can recover once"
    owner = "infra"

    def __init__(self) -> None:
        super().__init__()
        self.should_fail = True

    async def _on_plan(self, goal: str) -> ExecutionPlan:
        return ExecutionPlan(plan_id="plan-1")

    async def _on_execute(self, plan: ExecutionPlan) -> ExecutionResult:
        if self.should_fail:
            return ExecutionResult(
                plan_id="plan-1", success=False, error_message="Fatal fail"
            )
        return ExecutionResult(plan_id="plan-1", success=True)

    async def _on_recover(self, error: Exception) -> bool:
        self.should_fail = False
        return True


@pytest.mark.asyncio
async def test_supervisor_agent_recovery() -> None:
    """Verifies that the supervisor intercepts failure and retries."""
    agent = RecoverableAgent()
    supervisor = AgentSupervisor()

    plan = ExecutionPlan(plan_id="plan-1")

    # Define a custom execution fn mock
    runs = []

    async def execute_mock(p: ExecutionPlan) -> ExecutionResult:
        runs.append(p)
        return await agent._on_execute(p)

    res = await supervisor.oversee_execution(agent, plan, execute_mock)

    assert res.success is True
    assert len(runs) == 2  # Run 1 failed, run 2 succeeded
    assert supervisor.metrics["total_runs"] == 1
    assert supervisor.metrics["recovery_attempts"] == 1
    assert supervisor.metrics["successful_recoveries"] == 1
