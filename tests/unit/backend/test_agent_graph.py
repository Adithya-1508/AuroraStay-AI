import pytest
from pydantic import BaseModel

from backend.agents.executor.service import AgentExecutor
from backend.agents.graph.engine import GraphState, WorkflowEngine
from backend.agents.planner.service import AgentPlanner
from backend.ai.tools.executor import BaseTool, ToolExecutor


class ApprovalInput(BaseModel):
    goal: str


class SensitiveTool(BaseTool):
    name = "confirm_reservation"
    description = "A sensitive confirmation tool."
    args_schema = ApprovalInput

    async def _run(self, **kwargs: str) -> str:
        return "Confirmed: " + kwargs["goal"]


@pytest.mark.asyncio
async def test_workflow_engine_interruption() -> None:
    """Verifies that the graph engine interrupts on sensitive steps."""
    tool = SensitiveTool()
    tool_executor = ToolExecutor([tool])
    executor = AgentExecutor(tool_executor)
    planner = AgentPlanner(ai_service=None)

    engine = WorkflowEngine(planner, executor)

    # Launch graph execution
    config = {"configurable": {"thread_id": "thread-1"}}
    initial_state: GraphState = {
        "thread_id": "thread-1",
        "goal": "Test goal",
        "tools": ["confirm_reservation"],
        "plan_steps": [],
        "completed_steps": [],
        "current_step_idx": 0,
        "paused": False,
        "requires_approval": False,
        "approval_given": False,
        "error": None,
        "step_results": {},
        "success": False,
    }

    # Execute graph up to the interrupt point
    state = await engine.graph.ainvoke(initial_state, config)  # type: ignore[call-overload]

    # Pause before approval node on sensitive tools
    assert state.get("paused") is True
    assert state.get("requires_approval") is True
    assert len(state.get("completed_steps") or []) == 0

    # Resume the graph with approval_given=True
    resume_state = {
        "paused": False,
        "requires_approval": False,
        "approval_given": True,
    }
    final_state = await engine.graph.ainvoke(resume_state, config)  # type: ignore[call-overload]

    # Graph should now proceed, execute the tool, and complete successfully
    assert final_state.get("paused") is False
    assert final_state.get("success") is True
    assert len(final_state.get("completed_steps") or []) == 1
    assert (final_state.get("step_results") or {})["step_1"] == "Confirmed: Test goal"
