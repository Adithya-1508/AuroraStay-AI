import uuid

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.guest.api.routes import get_unit_of_work, router


@pytest.fixture
def test_app(db_session: AsyncSession) -> FastAPI:
    """Sets up a test FastAPI application with overridden database UOW dependency."""
    app = FastAPI()
    app.include_router(router)

    def override_get_unit_of_work() -> PostgresUnitOfWork:
        return PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore

    app.dependency_overrides[get_unit_of_work] = override_get_unit_of_work
    return app


@pytest.fixture
def client(test_app: FastAPI) -> TestClient:
    """Returns a TestClient configured for route controllers testing."""
    return TestClient(test_app)


def test_create_and_get_guest(client: TestClient) -> None:
    # 1. Create Guest
    payload = {
        "first_name": "Tony",
        "last_name": "Stark",
        "email": "tony@stark.com",
        "phone": "+1999999999",
        "loyalty_tier": "VIP",
    }
    response = client.post("/guests", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == "Tony"
    guest_id = data["id"]

    # 2. Get Guest
    response_get = client.get(f"/guests/{guest_id}")
    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json()["email"] == "tony@stark.com"


def test_guest_not_found(client: TestClient) -> None:
    fake_id = str(uuid.uuid4())
    response = client.get(f"/guests/{fake_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_preferences(client: TestClient) -> None:
    # Create Guest
    payload = {
        "first_name": "Bruce",
        "last_name": "Banner",
        "email": "bruce@avengers.com",
    }
    guest_id = client.post("/guests", json=payload).json()["id"]

    # Update preferences
    pref_payload = {
        "room_preferences": {"bed": "King"},
        "pillow_preferences": "Memory Foam",
        "dietary_restrictions": ["Gluten-Free"],
        "accessibility_requirements": [],
        "communication_preferences": {},
    }
    response = client.put(f"/guests/{guest_id}/preferences", json=pref_payload)
    assert response.status_code == status.HTTP_200_OK

    # Fetch preferences
    response_get = client.get(f"/guests/{guest_id}/preferences")
    assert response_get.json()["pillow_preferences"] == "Memory Foam"


def test_generate_recommendations(client: TestClient) -> None:
    # Create Guest
    payload = {
        "first_name": "Natasha",
        "last_name": "Romanoff",
        "email": "natasha@shield.gov",
        "loyalty_tier": "VIP",
    }
    guest_id = client.post("/guests", json=payload).json()["id"]

    # Get recommendations
    response = client.get(f"/guests/{guest_id}/recommendations")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 2


def test_concierge_chat_endpoints(client: TestClient) -> None:
    conversation_id = str(uuid.uuid4())

    # 1. Start Chat
    payload = {
        "conversation_id": conversation_id,
        "message": "Hello, when is check out?",
    }
    response = client.post("/concierge/chat", json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert "check-in" in response.json()["reply"].lower()

    # 2. Get Conversations list
    response_list = client.get("/conversations")
    assert response_list.status_code == status.HTTP_200_OK
    assert len(response_list.json()) >= 1

    # 3. Get Conversation details
    response_details = client.get(f"/conversations/{conversation_id}")
    assert response_details.status_code == status.HTTP_200_OK
    assert len(response_details.json()["messages"]) >= 2


def test_api_guest_edge_cases(client: TestClient) -> None:
    # 1. Create duplicate guest email raises Bad Request
    payload = {
        "first_name": "Tony",
        "last_name": "Stark",
        "email": "duplicate@stark.com",
    }
    response1 = client.post("/guests", json=payload)
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = client.post("/guests", json=payload)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST

    # 2. Update guest profile successfully
    guest_id = response1.json()["id"]
    response_update = client.put(f"/guests/{guest_id}", json={"first_name": "Anthony"})
    assert response_update.status_code == status.HTTP_200_OK
    assert response_update.json()["first_name"] == "Anthony"

    # 3. Update guest profile for non-existent guest returns 404
    fake_id = str(uuid.uuid4())
    response_fake_update = client.put(
        f"/guests/{fake_id}", json={"first_name": "Anthony"}
    )
    assert response_fake_update.status_code == status.HTTP_404_NOT_FOUND

    # 4. Get preferences for non-existent guest returns 404
    response_pref = client.get(f"/guests/{fake_id}/preferences")
    assert response_pref.status_code == status.HTTP_404_NOT_FOUND

    # 5. Update preferences for non-existent guest returns 404
    response_update_pref = client.put(f"/guests/{fake_id}/preferences", json={})
    assert response_update_pref.status_code == status.HTTP_404_NOT_FOUND

    # 6. Get recommendations for non-existent guest returns 404
    response_recs = client.get(f"/guests/{fake_id}/recommendations")
    assert response_recs.status_code == status.HTTP_404_NOT_FOUND

    # 7. Get conversation that does not exist returns 404
    response_conv = client.get(f"/conversations/{fake_id}")
    assert response_conv.status_code == status.HTTP_404_NOT_FOUND


def test_dependency_provider() -> None:
    uow = get_unit_of_work()
    assert isinstance(uow, PostgresUnitOfWork)


@pytest.mark.asyncio
async def test_routes_directly(db_session: AsyncSession) -> None:
    from fastapi import HTTPException

    from business.guest.api.routes import (
        ConciergeChatRequest,
        GuestProfileCreate,
        GuestProfileUpdate,
        PreferenceSetUpdate,
        concierge_chat,
        create_guest,
        get_conversation,
        get_guest,
        get_guest_preferences,
        get_guest_recommendations,
        list_conversations,
        update_guest,
        update_guest_preferences,
    )

    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore

    # 1. create_guest
    req = GuestProfileCreate(
        first_name="Direct", last_name="Call", email="direct@example.com"
    )
    res = await create_guest(req, uow)
    guest_uuid = uuid.UUID(res["id"])
    assert res["first_name"] == "Direct"

    # create duplicate email to trigger ValueError / Bad Request HTTP exception
    with pytest.raises(HTTPException) as exc:
        await create_guest(req, uow)
    assert exc.value.status_code == 400

    # 2. get_guest
    res_get = await get_guest(guest_uuid, uow)
    assert res_get["email"] == "direct@example.com"

    # get_guest non-existent
    with pytest.raises(HTTPException) as exc:
        await get_guest(uuid.uuid4(), uow)
    assert exc.value.status_code == 404

    # 3. update_guest
    up_req = GuestProfileUpdate(first_name="Directed")
    res_up = await update_guest(guest_uuid, up_req, uow)
    assert res_up["first_name"] == "Directed"

    # update_guest non-existent
    with pytest.raises(HTTPException) as exc:
        await update_guest(uuid.uuid4(), up_req, uow)
    assert exc.value.status_code == 404

    # 4. update_guest_preferences
    pref_req = PreferenceSetUpdate(pillow_preferences="Foam")
    res_pref = await update_guest_preferences(guest_uuid, pref_req, uow)
    assert "updated successfully" in res_pref["message"]

    # update_guest_preferences non-existent
    with pytest.raises(HTTPException) as exc:
        await update_guest_preferences(uuid.uuid4(), pref_req, uow)
    assert exc.value.status_code == 404

    # 5. get_guest_preferences
    res_pref_get = await get_guest_preferences(guest_uuid, uow)
    assert res_pref_get["pillow_preferences"] == "Foam"

    # get_guest_preferences non-existent
    with pytest.raises(HTTPException) as exc:
        await get_guest_preferences(uuid.uuid4(), uow)
    assert exc.value.status_code == 404

    # 6. get_guest_recommendations
    res_recs = await get_guest_recommendations(guest_uuid, uow)
    assert len(res_recs) == 1

    # get_guest_recommendations non-existent
    with pytest.raises(HTTPException) as exc:
        await get_guest_recommendations(uuid.uuid4(), uow)
    assert exc.value.status_code == 404

    # 7. concierge_chat
    chat_req = ConciergeChatRequest(
        conversation_id=uuid.uuid4(), guest_id=guest_uuid, message="When is check-out?"
    )
    res_chat = await concierge_chat(chat_req, uow)
    assert "reply" in res_chat

    # concierge_chat non-existent guest
    chat_req_fake = ConciergeChatRequest(
        conversation_id=uuid.uuid4(), guest_id=uuid.uuid4(), message="I want a queen bed"
    )
    with pytest.raises(HTTPException) as exc:
        await concierge_chat(chat_req_fake, uow)
    assert exc.value.status_code == 404

    # 8. list_conversations
    convs = await list_conversations(uow)
    assert len(convs) >= 1

    # 9. get_conversation
    conv_id = chat_req.conversation_id
    res_conv = await get_conversation(conv_id, uow)
    assert res_conv["id"] == str(conv_id)

    # get_conversation non-existent
    with pytest.raises(HTTPException) as exc:
        await get_conversation(uuid.uuid4(), uow)
    assert exc.value.status_code == 404
