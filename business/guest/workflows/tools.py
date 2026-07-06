import uuid
from typing import Any

from pydantic import BaseModel, Field

from backend.ai.tools.executor import BaseTool
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.guest.domain.value_objects import PreferenceSet
from business.guest.services.concierge import ConciergeService
from business.guest.services.preferences import PreferenceLearningEngine
from business.guest.services.recommendations import RecommendationEngine

# --- Input Schemas ---


class SearchHotelKnowledgeInput(BaseModel):
    query: str = Field(
        ...,
        description="The query string to search in the hotel FAQ and knowledge base.",
    )


class FindRestaurantInput(BaseModel):
    cuisine: str | None = Field(
        None, description="Optional cuisine filter (e.g. Italian, Indian, French)."
    )


class FindSpaServiceInput(BaseModel):
    service_type: str | None = Field(
        None, description="Optional service type filter (e.g., Massage, Facial)."
    )


class RecommendFacilityInput(BaseModel):
    guest_id: uuid.UUID = Field(
        ..., description="The UUID of the guest to generate recommendations for."
    )


class ReservationLookupInput(BaseModel):
    guest_email: str = Field(
        ..., description="The email of the guest to search reservations for."
    )


class GuestPreferenceInput(BaseModel):
    guest_id: uuid.UUID = Field(..., description="The UUID of the guest.")
    pillow_preferences: str | None = Field(
        None, description="Optional pillow preference update."
    )
    dietary_restrictions: list[str] | None = Field(
        None, description="Optional list of dietary restrictions."
    )


class EscalateToStaffInput(BaseModel):
    guest_id: uuid.UUID = Field(..., description="The UUID of the guest.")
    conversation_id: uuid.UUID = Field(
        ..., description="The UUID of the conversation session."
    )
    reason: str = Field(..., description="The reason for escalations.")


# --- Tool Implementations ---


class SearchHotelKnowledgeTool(BaseTool):
    name = "SearchHotelKnowledgeTool"
    description = (
        "Searches the hotel policy, FAQ, and general knowledge base for answers."
    )
    args_schema = SearchHotelKnowledgeInput

    async def _run(self, **kwargs: Any) -> Any:
        query = kwargs["query"]
        async with PostgresUnitOfWork() as uow:
            pref_engine = PreferenceLearningEngine(uow)
            concierge = ConciergeService(uow, pref_engine)
            res = await concierge.chat(uuid.uuid4(), None, query)
            return {
                "answer": res["reply"],
                "citations": res["citations"],
            }


class FindRestaurantTool(BaseTool):
    name = "FindRestaurantTool"
    description = "Finds restaurants located inside the hotel or nearby, listing opening hours and menus."
    args_schema = FindRestaurantInput

    async def _run(self, **kwargs: Any) -> Any:
        cuisine = kwargs.get("cuisine")
        # Direct mock facility directory
        restaurants = [
            {
                "name": "Aurora Bistro",
                "cuisine": "French/Modern",
                "hours": "7:00 AM - 10:00 PM",
                "location": "Lobby level",
            },
            {
                "name": "Zen Noodles",
                "cuisine": "Asian",
                "hours": "12:00 PM - 11:00 PM",
                "location": "1st Floor",
            },
            {
                "name": "Bella Vista",
                "cuisine": "Italian",
                "hours": "6:00 PM - 11:00 PM",
                "location": "Rooftop terrace",
            },
        ]
        if cuisine:
            restaurants = [
                r for r in restaurants if cuisine.lower() in r["cuisine"].lower()
            ]
        return {"restaurants": restaurants}


class FindSpaServiceTool(BaseTool):
    name = "FindSpaServiceTool"
    description = "Searches for available spa therapies, massages, and pool facility opening hours."
    args_schema = FindSpaServiceInput

    async def _run(self, **kwargs: Any) -> Any:
        service_type = kwargs.get("service_type")
        services = [
            {
                "name": "Zen Premium Spa Therapy",
                "duration": "60 mins",
                "price": "$120",
                "description": "Relaxing full body massage",
            },
            {
                "name": "Radiant Facial",
                "duration": "45 mins",
                "price": "$90",
                "description": "Cleansing skin facial",
            },
            {
                "name": "Hot Stone Massage",
                "duration": "90 mins",
                "price": "$180",
                "description": "Stress-melting hot basalt stones treatment",
            },
        ]
        if service_type:
            services = [
                s
                for s in services
                if service_type.lower() in s["name"].lower()
                or service_type.lower() in s["description"].lower()
            ]
        return {"spa_services": services}


class RecommendFacilityTool(BaseTool):
    name = "RecommendFacilityTool"
    description = (
        "Generates personalized dining, spa, and room upgrade suggestions for a guest."
    )
    args_schema = RecommendFacilityInput

    async def _run(self, **kwargs: Any) -> Any:
        guest_id = kwargs["guest_id"]
        async with PostgresUnitOfWork() as uow:
            engine = RecommendationEngine(uow)
            recs = await engine.generate_recommendations(guest_id)
            return {
                "recommendations": [
                    {"item_type": r.item_type, "score": float(r.score)} for r in recs
                ]
            }


class ReservationLookupTool(BaseTool):
    name = "ReservationLookupTool"
    description = "Queries active stay details and booking context for a guest using their email address."
    args_schema = ReservationLookupInput

    async def _run(self, **kwargs: Any) -> Any:
        email = kwargs["guest_email"]
        async with PostgresUnitOfWork() as uow:
            guest = await uow.guests.get_by_email(email)
            if not guest:
                return {"message": "No guest profile found for this email."}

            reservations = await uow.reservations.get_all()
            guest_res = [
                {
                    "reservation_id": str(r.id),
                    "check_in": r.check_in_date.isoformat(),
                    "check_out": r.check_out_date.isoformat(),
                    "status": r.status,
                }
                for r in reservations
                if r.guest_id == guest.id
            ]
            return {"reservations": guest_res}


class GuestPreferenceTool(BaseTool):
    name = "GuestPreferenceTool"
    description = (
        "Explicitly registers or updates pillow and dietary preferences for a guest."
    )
    args_schema = GuestPreferenceInput

    async def _run(self, **kwargs: Any) -> Any:
        guest_id = kwargs["guest_id"]
        pillow = kwargs.get("pillow_preferences")
        dietary = kwargs.get("dietary_restrictions")

        async with PostgresUnitOfWork() as uow:
            engine = PreferenceLearningEngine(uow)
            current_prefs = await engine.get_preferences(guest_id)

            updated_prefs = PreferenceSet(
                room_preferences=current_prefs.room_preferences,
                pillow_preferences=pillow or current_prefs.pillow_preferences,
                dietary_restrictions=dietary or current_prefs.dietary_restrictions,
                accessibility_requirements=current_prefs.accessibility_requirements,
                communication_preferences=current_prefs.communication_preferences,
            )
            await engine.update_preferences(guest_id, updated_prefs)
            return {"message": "Preferences updated successfully."}


class EscalateToStaffTool(BaseTool):
    name = "EscalateToStaffTool"
    description = "Escalates a guest conversation session to human hotel staff for immediate assistance."
    args_schema = EscalateToStaffInput

    async def _run(self, **kwargs: Any) -> Any:
        guest_id = kwargs["guest_id"]
        conversation_id = kwargs["conversation_id"]
        reason = kwargs["reason"]

        async with PostgresUnitOfWork() as uow:
            pref_engine = PreferenceLearningEngine(uow)
            concierge = ConciergeService(uow, pref_engine)
            await concierge.chat(conversation_id, guest_id, f"Escalate: {reason}")
            return {
                "escalated": True,
                "message": "Human staff notified. They will contact you shortly.",
            }
