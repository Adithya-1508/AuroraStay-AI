import json

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.ai.providers.mock import MockProvider
from backend.models.guest import Guest
from backend.models.room import Room, RoomCategory
from business.reservation.workflows.agent import ReservationAssistantAgent


@pytest.mark.asyncio
async def test_reservation_assistant_chat_flow(
    db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verifies conversational chat and tool-calling execution for the assistant agent."""
    # 1. Seed DB
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.flush()

    room = Room(room_number="101", category_id=cat.id, status="Available")
    guest = Guest(
        first_name="Alexandra",
        last_name="Smith",
        email="alex@gmail.com",
        loyalty_tier="Bronze",
    )
    db_session.add_all([room, guest])
    await db_session.flush()

    # 2. Instantiate and initialize agent
    agent = ReservationAssistantAgent()
    await agent.initialize()

    # Override db session factory for testing inside agent executors
    def mock_factory() -> AsyncSession:
        return db_session

    # Override session factory on the PostgresUnitOfWork used inside tools
    # By mocking PostgresUnitOfWork's instantiation using monkeypatch:
    from backend.repositories.unit_of_work import PostgresUnitOfWork

    old_init = PostgresUnitOfWork.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, session_factory=mock_factory)

    monkeypatch.setattr(PostgresUnitOfWork, "__init__", new_init)

    # 3. Configure mock LLM response representing the planner plan
    mock_plan = {
        "steps": [
            {
                "step_id": "step_1",
                "name": "check_avail",
                "tool": "SearchAvailabilityTool",
                "arguments": {
                    "check_in_date": "2026-07-10",
                    "check_out_date": "2026-07-15",
                    "category_name": "Standard",
                },
            }
        ],
        "dependencies": {},
    }

    mock_prov: MockProvider = agent.providers.get("mock")  # type: ignore
    mock_prov.add_response(content=json.dumps(mock_plan))

    # 4. Invoke agent chat
    res = await agent.chat(
        session_id="test-session-123",
        message="I want to check standard room availability from 2026-07-10 to 2026-07-15.",
    )

    # 5. Assertions
    assert res["success"] is True
    assert "step_1" in res["completed_steps"]
    step_res = res["step_results"]["step_1"]
    assert step_res["available"] is True
    assert step_res["category_name"] == "Standard"
