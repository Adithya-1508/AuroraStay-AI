import pytest
from pydantic import BaseModel

from backend.agents.core.base_agent import ExecutionPlan, ExecutionStep
from backend.agents.executor.service import AgentExecutor
from backend.ai.tools.executor import BaseTool, ToolExecutor


class DummyInput(BaseModel):
    goal: str


class DummyTool(BaseTool):
    name = "dummy_tool"
    description = "Test tool"
    args_schema = DummyInput

    async def _run(self, **kwargs: str) -> str:
        return "Success: " + kwargs["goal"]


@pytest.mark.asyncio
async def test_agent_executor_plan_runs() -> None:
    """Verifies that the executor runs plan steps in order and captures results."""
    tool = DummyTool()
    tool_executor = ToolExecutor([tool])
    executor = AgentExecutor(tool_executor)

    # Construct execution steps
    step1 = ExecutionStep(
        step_id="step_1",
        name="step_one",
        tool="dummy_tool",
        arguments={"goal": "first-goal"},
    )
    step2 = ExecutionStep(
        step_id="step_2",
        name="step_two",
        tool="dummy_tool",
        arguments={"goal": "second-goal"},
    )

    plan = ExecutionPlan(
        plan_id="plan-x",
        steps=[step1, step2],
        dependencies={"step_2": ["step_1"]},
    )

    result = await executor.execute_plan(plan)
    assert result.success is True
    assert result.step_results["step_1"] == "Success: first-goal"
    assert result.step_results["step_2"] == "Success: second-goal"
