import uuid
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.agents.core.base_agent import ExecutionPlan, ExecutionResult
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.guest.domain.value_objects import ProfileDetails
from business.guest.services.profile import GuestProfileService
from business.guest.workflows.agent import GuestConciergeAgent
from business.guest.workflows.tools import (
    EscalateToStaffTool,
    FindRestaurantTool,
    FindSpaServiceTool,
    GuestPreferenceTool,
    RecommendFacilityTool,
    ReservationLookupTool,
    SearchHotelKnowledgeTool,
)


@pytest.mark.asyncio
async def test_guest_concierge_agent_capabilities() -> None:
    # Test initialization and capabilities listing
    agent = GuestConciergeAgent()
    await agent.initialize()
    assert agent.name == "GuestConcierge"
    assert "Search hotel policy and FAQs" in agent.capabilities
    assert "SearchHotelKnowledgeTool" in agent.required_tools


@pytest.mark.asyncio
async def test_restaurant_and_spa_tools() -> None:
    # 1. FindRestaurantTool
    restaurant_tool = FindRestaurantTool()
    res_dining = await restaurant_tool._run(cuisine="Italian")
    assert len(res_dining["restaurants"]) == 1
    assert res_dining["restaurants"][0]["name"] == "Bella Vista"

    # 2. FindSpaServiceTool
    spa_tool = FindSpaServiceTool()
    res_spa = await spa_tool._run(service_type="massage")
    assert len(res_spa["spa_services"]) == 2
    assert res_spa["spa_services"][0]["name"] == "Zen Premium Spa Therapy"


@pytest.mark.asyncio
async def test_guest_profile_linked_tools(db_session: AsyncSession) -> None:
    # Override session factory so tools query our in-memory DB

    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    profile_service = GuestProfileService(uow)
    guest = await profile_service.create_profile(
        ProfileDetails(first_name="Terry", last_name="Crews", email="terry@example.com")
    )

    # 1. RecommendFacilityTool
    rec_tool = RecommendFacilityTool()
    res_rec = await rec_tool._run(guest_id=guest.id)
    assert len(res_rec["recommendations"]) == 1  # Spa therapist default

    # 2. GuestPreferenceTool
    pref_tool = GuestPreferenceTool()
    await pref_tool._run(
        guest_id=guest.id,
        pillow_preferences="Feather",
        dietary_restrictions=["Vegan"],
    )
    # Check preferences updated
    async with uow:
        db_guest = await uow.guests.get(str(guest.id))
        assert db_guest is not None
        assert db_guest.preferences is not None
        assert db_guest.preferences.get("pillow_preferences") == "Feather"
        assert "Vegan" in db_guest.preferences.get("dietary_restrictions", [])

    # 3. ReservationLookupTool
    lookup_tool = ReservationLookupTool()
    res_lookup = await lookup_tool._run(guest_email="terry@example.com")
    assert "reservations" in res_lookup
    assert len(res_lookup["reservations"]) == 0  # No reservations created yet

    # 4. EscalateToStaffTool
    escalate_tool = EscalateToStaffTool()
    res_escalate = await escalate_tool._run(
        guest_id=guest.id,
        conversation_id=uuid.uuid4(),
        reason="My AC is not working",
    )
    assert res_escalate["escalated"] is True

    # 5. SearchHotelKnowledgeTool
    search_tool = SearchHotelKnowledgeTool()
    res_search = await search_tool._run(query="What is check in time?")
    assert "check-in" in res_search["answer"].lower()

    # 6. ReservationLookupTool with non-existent email
    res_lookup_fake = await lookup_tool._run(guest_email="nonexistent@example.com")
    assert "No guest profile found" in res_lookup_fake["message"]


@pytest.mark.asyncio
async def test_guest_concierge_agent_planning_and_execution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # 1. Setup agent and initialize
    agent = GuestConciergeAgent()
    await agent.initialize()

    # 2. Mock Planner create_plan
    async def mock_create_plan(*args: Any, **kwargs: Any) -> ExecutionPlan:
        return ExecutionPlan(plan_id="plan-123", steps=[])

    monkeypatch.setattr(agent.planner, "create_plan", mock_create_plan)

    # Test _on_plan
    plan = await agent._on_plan("Hello")
    assert len(plan.steps) == 0

    # 3. Mock Executor execute_plan
    async def mock_execute_plan(*args: Any, **kwargs: Any) -> ExecutionResult:
        return ExecutionResult(plan_id="plan-123", success=True)

    monkeypatch.setattr(agent.executor, "execute_plan", mock_execute_plan)

    # Test _on_execute
    res = await agent._on_execute(plan)
    assert res.success is True

    # 4. Mock LangGraph engine ainvoke
    async def mock_ainvoke(state: Any, config: Any = None) -> Any:
        state["success"] = True
        return state

    monkeypatch.setattr(agent.engine.graph, "ainvoke", mock_ainvoke)

    # Test chat route
    chat_res = await agent.chat(session_id="session-123", message="Howdy")
    assert chat_res["success"] is True
