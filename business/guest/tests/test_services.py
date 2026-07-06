import uuid
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.guest.domain.exceptions import GuestNotFoundError
from business.guest.domain.value_objects import PreferenceSet, ProfileDetails
from business.guest.services.concierge import ConciergeService
from business.guest.services.preferences import PreferenceLearningEngine
from business.guest.services.profile import GuestProfileService
from business.guest.services.recommendations import RecommendationEngine


@pytest.mark.asyncio
async def test_guest_profile_service(db_session: AsyncSession) -> None:
    # Setup UOW
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    service = GuestProfileService(uow)

    # 1. Create Profile
    details = ProfileDetails(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="+1234567890",
    )
    guest = await service.create_profile(details, loyalty_tier="Gold")
    assert guest.id is not None
    assert guest.first_name == "Jane"
    assert guest.loyalty_tier == "Gold"

    # 2. Get Profile
    fetched = await service.get_profile(guest.id)
    assert fetched.email == "jane.doe@example.com"

    # 3. Update Profile
    updated = await service.update_profile(
        guest.id, {"first_name": "Janet", "loyalty_tier": "Platinum"}
    )
    assert updated.first_name == "Janet"
    assert updated.loyalty_tier == "Platinum"

    # 4. Error Case (Not Found)
    with pytest.raises(GuestNotFoundError):
        await service.get_profile(uuid.uuid4())


@pytest.mark.asyncio
async def test_preference_learning_engine(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    profile_service = GuestProfileService(uow)
    pref_engine = PreferenceLearningEngine(uow)

    details = ProfileDetails(
        first_name="John", last_name="Smith", email="john.smith@example.com"
    )
    guest = await profile_service.create_profile(details)

    # Explicit Update
    new_prefs = PreferenceSet(
        room_preferences={"floor": "High"},
        pillow_preferences="Feather",
        dietary_restrictions=["Vegan"],
    )
    await pref_engine.update_preferences(guest.id, new_prefs)

    fetched = await pref_engine.get_preferences(guest.id)
    assert fetched.pillow_preferences == "Feather"
    assert "Vegan" in fetched.dietary_restrictions

    # Learn from text
    await pref_engine.learn_preferences_from_text(
        guest.id,
        "I would love a memory foam pillow and a king size bed, also please make sure food is vegetarian",
    )
    learned = await pref_engine.get_preferences(guest.id)
    assert learned.pillow_preferences == "Memory Foam"
    assert learned.room_preferences.get("bed_type") == "King"
    assert "Vegetarian" in learned.dietary_restrictions


@pytest.mark.asyncio
async def test_recommendation_engine(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    profile_service = GuestProfileService(uow)
    pref_engine = PreferenceLearningEngine(uow)
    rec_engine = RecommendationEngine(uow)

    guest = await profile_service.create_profile(
        ProfileDetails(
            first_name="Alice", last_name="Wonder", email="alice@example.com"
        ),
        loyalty_tier="VIP",
    )
    await pref_engine.update_preferences(
        guest.id, PreferenceSet(dietary_restrictions=["Vegetarian"])
    )

    # Generate Recs
    recs = await rec_engine.generate_recommendations(guest.id)
    assert len(recs) == 3
    types = [r.item_type for r in recs]
    assert "Room Upgrade" in types
    assert "Vegetarian Dining at Aurora Bistro" in types
    assert "Zen Premium Spa Therapy" in types

    # Fetch List
    list_recs = await rec_engine.get_guest_recommendations(guest.id)
    assert len(list_recs) == 3


@pytest.mark.asyncio
async def test_concierge_service(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    profile_service = GuestProfileService(uow)
    pref_engine = PreferenceLearningEngine(uow)
    concierge = ConciergeService(uow, pref_engine)

    guest = await profile_service.create_profile(
        ProfileDetails(first_name="Bob", last_name="Builder", email="bob@example.com")
    )
    conversation_id = uuid.uuid4()

    # Chat - standard FAQ fallback
    res = await concierge.chat(conversation_id, guest.id, "What is checkout policy?")
    assert "check-in time is at 3:00 PM" in res["reply"]
    assert "FAQ_HotelPolicy_v1_p1" in res["citations"]

    # Chat - service booking (Room Service)
    res_service = await concierge.chat(
        conversation_id, guest.id, "Can I get room service?"
    )
    assert "submitted your room service request" in res_service["reply"]
    assert "room_service_request" in res_service["actions"]

    # Chat - escalation
    res_escalate = await concierge.chat(
        conversation_id, guest.id, "Please escalate to a manager."
    )
    assert "escalating your request" in res_escalate["reply"]
    assert res_escalate["escalated"] is True


@pytest.mark.asyncio
async def test_guest_profile_service_edge_cases(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    service = GuestProfileService(uow)

    # 1. Duplicate email registration raises ValueError
    details = ProfileDetails(
        first_name="Double", last_name="Agent", email="double@example.com"
    )
    await service.create_profile(details)
    with pytest.raises(ValueError, match="already registered"):
        await service.create_profile(details)

    # 2. Get profile by email
    found = await service.get_profile_by_email("double@example.com")
    assert found.first_name == "Double"

    # 3. Get profile by non-existent email raises GuestNotFoundError
    with pytest.raises(GuestNotFoundError):
        await service.get_profile_by_email("nonexistent@example.com")

    # 4. Update profile for non-existent guest raises GuestNotFoundError
    with pytest.raises(GuestNotFoundError):
        await service.update_profile(uuid.uuid4(), {"first_name": "Ghost"})


@pytest.mark.asyncio
async def test_preference_learning_engine_edge_cases(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    pref_engine = PreferenceLearningEngine(uow)
    profile_service = GuestProfileService(uow)

    guest = await profile_service.create_profile(
        ProfileDetails(first_name="Key", last_name="Word", email="keyword@example.com")
    )

    # 1. Non-existent guest exception checks
    non_existent = uuid.uuid4()
    with pytest.raises(GuestNotFoundError):
        await pref_engine.get_preferences(non_existent)
    with pytest.raises(GuestNotFoundError):
        await pref_engine.update_preferences(non_existent, PreferenceSet())
    with pytest.raises(GuestNotFoundError):
        await pref_engine.learn_preferences_from_text(non_existent, "queen bed")

    # 2. Keywords preference learning combinations
    await pref_engine.learn_preferences_from_text(
        guest.id,
        "I need a queen bed on a low floor, vegan, gluten-free, feather pillow",
    )
    learned = await pref_engine.get_preferences(guest.id)
    assert learned.room_preferences.get("bed_type") == "Queen"
    assert learned.room_preferences.get("floor") == "Low"
    assert learned.pillow_preferences == "Feather"
    assert "Vegan" in learned.dietary_restrictions
    assert "Gluten-Free" in learned.dietary_restrictions


@pytest.mark.asyncio
async def test_recommendation_engine_edge_cases(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    rec_engine = RecommendationEngine(uow)

    non_existent = uuid.uuid4()
    with pytest.raises(GuestNotFoundError):
        await rec_engine.generate_recommendations(non_existent)
    with pytest.raises(GuestNotFoundError):
        await rec_engine.get_guest_recommendations(non_existent)


@pytest.mark.asyncio
async def test_concierge_service_edge_cases(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    profile_service = GuestProfileService(uow)
    pref_engine = PreferenceLearningEngine(uow)

    # RAG exception mock retriever
    class ExceptionRetriever:
        async def retrieve(self, text: str) -> list[dict[str, Any]]:
            raise RuntimeError("Database timeout during RAG retrieval")

    concierge = ConciergeService(uow, pref_engine, retriever=ExceptionRetriever())

    guest = await profile_service.create_profile(
        ProfileDetails(
            first_name="Trouble", last_name="Maker", email="trouble@example.com"
        )
    )
    conversation_id = uuid.uuid4()

    # 1. Chat with spa booking
    res_spa = await concierge.chat(
        conversation_id, guest.id, "Please book a spa massage session."
    )
    assert "book_spa" in res_spa["actions"]

    # 2. Chat with maintenance issue
    res_issue = await concierge.chat(
        conversation_id, guest.id, "My room sink is leaking and broken."
    )
    assert "report_issue" in res_issue["actions"]

    # 3. Chat with retriever failure (falls back to local policy)
    res_fallback = await concierge.chat(
        conversation_id, guest.id, "What is the checkout policy?"
    )
    assert "FAQ_HotelPolicy_v1_p1" in res_fallback["citations"]
