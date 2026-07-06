import pytest

from backend.agents.planner.service import AgentPlanner


@pytest.mark.asyncio
async def test_agent_planner_heuristics() -> None:
    """Verifies that the planner falls back without AI service."""
    planner = AgentPlanner(ai_service=None)
    available_tools = ["get_guest", "update_reservation"]

    plan = await planner.create_plan(
        goal="Update reservation for guest 101",
        available_tools=available_tools,
    )

    assert plan.plan_id is not None
    assert len(plan.steps) == 2
    assert plan.steps[0].tool == "get_guest"
    assert plan.steps[1].tool == "update_reservation"

    # Verify dependency links are sequential
    dependencies = plan.dependencies
    assert dependencies["step_2"] == ["step_1"]
