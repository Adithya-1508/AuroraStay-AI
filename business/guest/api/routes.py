from typing import Any
from uuid import UUID
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.models.conversation import Conversation
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.guest.domain.exceptions import (
    GuestDomainError,
    GuestNotFoundError,
)
from business.guest.domain.value_objects import PreferenceSet, ProfileDetails
from business.guest.services.concierge import ConciergeService
from business.guest.services.preferences import PreferenceLearningEngine
from business.guest.services.profile import GuestProfileService
from business.guest.services.recommendations import RecommendationEngine

router = APIRouter()


def get_unit_of_work() -> PostgresUnitOfWork:
    """Dependency injector resolving concrete PostgresUnitOfWork transactions."""
    return PostgresUnitOfWork()


# --- Request/Response Models ---


class GuestProfileCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    loyalty_tier: str = "Bronze"


class GuestProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    loyalty_tier: str | None = None


class PreferenceSetUpdate(BaseModel):
    room_preferences: dict[str, str] = Field(default_factory=dict)
    pillow_preferences: str | None = None
    dietary_restrictions: list[str] = Field(default_factory=list)
    accessibility_requirements: list[str] = Field(default_factory=list)
    communication_preferences: dict[str, str] = Field(default_factory=dict)


class ConciergeChatRequest(BaseModel):
    conversation_id: UUID
    guest_id: UUID | None = None
    message: str


# --- Endpoints ---


@router.post("/guests", status_code=status.HTTP_201_CREATED)
async def create_guest(
    request: GuestProfileCreate, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    """Registers a new guest profile."""
    service = GuestProfileService(uow)
    try:
        details = ProfileDetails(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
        )
        guest = await service.create_profile(details, request.loyalty_tier)
        return {
            "id": str(guest.id),
            "first_name": guest.first_name,
            "last_name": guest.last_name,
            "email": guest.email,
            "phone": guest.phone,
            "loyalty_tier": guest.loyalty_tier,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except GuestDomainError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e


@router.get("/guests/{id}")
async def get_guest(
    id: UUID, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    """Retrieves a guest profile by UUID."""
    service = GuestProfileService(uow)
    try:
        guest = await service.get_profile(id)
        return {
            "id": str(guest.id),
            "first_name": guest.first_name,
            "last_name": guest.last_name,
            "email": guest.email,
            "phone": guest.phone,
            "loyalty_tier": guest.loyalty_tier,
        }
    except GuestNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put("/guests/{id}")
async def update_guest(
    id: UUID,
    request: GuestProfileUpdate,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Updates fields on an existing guest profile."""
    service = GuestProfileService(uow)
    try:
        updates = {k: v for k, v in request.model_dump().items() if v is not None}
        guest = await service.update_profile(id, updates)
        return {
            "id": str(guest.id),
            "first_name": guest.first_name,
            "last_name": guest.last_name,
            "email": guest.email,
            "phone": guest.phone,
            "loyalty_tier": guest.loyalty_tier,
        }
    except GuestNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get("/guests/{id}/preferences")
async def get_guest_preferences(
    id: UUID, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    """Retrieves dynamic preferences for a guest."""
    engine = PreferenceLearningEngine(uow)
    try:
        prefs = await engine.get_preferences(id)
        return {
            "room_preferences": prefs.room_preferences,
            "pillow_preferences": prefs.pillow_preferences,
            "dietary_restrictions": prefs.dietary_restrictions,
            "accessibility_requirements": prefs.accessibility_requirements,
            "communication_preferences": prefs.communication_preferences,
        }
    except GuestNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.put("/guests/{id}/preferences")
async def update_guest_preferences(
    id: UUID,
    request: PreferenceSetUpdate,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Updates preferences for a guest."""
    engine = PreferenceLearningEngine(uow)
    try:
        new_prefs = PreferenceSet(
            room_preferences=request.room_preferences,
            pillow_preferences=request.pillow_preferences,
            dietary_restrictions=request.dietary_restrictions,
            accessibility_requirements=request.accessibility_requirements,
            communication_preferences=request.communication_preferences,
        )
        await engine.update_preferences(id, new_prefs)
        return {"message": "Preferences updated successfully."}
    except GuestNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get("/guests/{id}/recommendations")
async def get_guest_recommendations(
    id: UUID, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> list[dict[str, Any]]:
    """Retrieves generated recommendations for a guest."""
    engine = RecommendationEngine(uow)
    try:
        recs = await engine.generate_recommendations(id)
        return [
            {
                "id": str(r.id),
                "item_type": r.item_type,
                "score": float(r.score),
                "is_accepted": r.is_accepted,
                "generated_at": r.generated_at.isoformat(),
            }
            for r in recs
        ]
    except GuestNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.post("/concierge/chat")
async def concierge_chat(
    request: ConciergeChatRequest, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    """Processes conversational messages using the AI Concierge service."""
    pref_engine = PreferenceLearningEngine(uow)
    service = ConciergeService(uow, pref_engine)
    try:
        result = await service.chat(
            request.conversation_id, request.guest_id, request.message
        )
        return result
    except GuestNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get("/conversations")
async def list_conversations(
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> list[dict[str, Any]]:
    """Lists conversation sessions."""
    async with uow:
        result = await uow.session.execute(select(Conversation))
        convs = result.scalars().all()
        return [
            {
                "id": str(c.id),
                "guest_id": str(c.guest_id) if c.guest_id else None,
                "channel": c.channel,
            }
            for c in convs
        ]


@router.get("/conversations/{id}")
async def get_conversation(
    id: UUID, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    """Retrieves the message log and metadata of a specific conversation session."""
    async with uow:
        db_conv = await uow.session.get(Conversation, id)
        if not db_conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation session '{id}' was not found.",
            ) from None
        messages_list = []
        if isinstance(db_conv.messages, dict) and "messages" in db_conv.messages:
            messages_list = db_conv.messages["messages"]
        return {
            "id": str(db_conv.id),
            "guest_id": str(db_conv.guest_id) if db_conv.guest_id else None,
            "channel": db_conv.channel,
            "messages": messages_list,
        }
