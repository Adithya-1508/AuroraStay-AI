import uuid

from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.guest.domain.exceptions import GuestNotFoundError
from business.guest.domain.value_objects import PreferenceSet
from business.guest.events.publisher import domain_event_publisher
from business.guest.events.schemas import PreferenceChanged


class PreferenceLearningEngine:
    """Service to load, modify, and learn preferences from conversational guest inputs."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def get_preferences(self, guest_id: uuid.UUID) -> PreferenceSet:
        """Retrieves structured preferences for a guest."""
        async with self.uow:
            guest = await self.uow.guests.get(str(guest_id))
            if not guest:
                raise GuestNotFoundError(str(guest_id))

            prefs = guest.preferences or {}
            return PreferenceSet(
                room_preferences=prefs.get("room_preferences", {}),
                pillow_preferences=prefs.get("pillow_preferences"),
                dietary_restrictions=prefs.get("dietary_restrictions", []),
                accessibility_requirements=prefs.get("accessibility_requirements", []),
                communication_preferences=prefs.get("communication_preferences", {}),
            )

    async def update_preferences(
        self, guest_id: uuid.UUID, new_prefs: PreferenceSet
    ) -> None:
        """Explicitly sets or overwrites preferences for a guest."""
        async with self.uow:
            guest = await self.uow.guests.get(str(guest_id))
            if not guest:
                raise GuestNotFoundError(str(guest_id))

            old_prefs = guest.preferences or {}
            updated_prefs = {
                "room_preferences": new_prefs.room_preferences,
                "pillow_preferences": new_prefs.pillow_preferences,
                "dietary_restrictions": new_prefs.dietary_restrictions,
                "accessibility_requirements": new_prefs.accessibility_requirements,
                "communication_preferences": new_prefs.communication_preferences,
            }

            guest.preferences = updated_prefs
            await self.uow.commit()

            # Publish event
            changes = {}
            if old_prefs.get("pillow_preferences") != new_prefs.pillow_preferences:
                changes["pillow_preferences"] = str(new_prefs.pillow_preferences)
            if old_prefs.get("dietary_restrictions") != new_prefs.dietary_restrictions:
                changes["dietary_restrictions"] = str(new_prefs.dietary_restrictions)

            if changes:
                await domain_event_publisher.publish(
                    PreferenceChanged(
                        guest_id=guest.id,
                        changed_preferences=changes,
                    )
                )

    async def learn_preferences_from_text(self, guest_id: uuid.UUID, text: str) -> None:
        """Parses text dynamically and learns/updates preference rules."""
        text_lower = text.lower()
        room_prefs = {}
        dietary = []
        pillow = None

        # Basic keyword parsing rules
        if "king bed" in text_lower or "king size" in text_lower:
            room_prefs["bed_type"] = "King"
        elif "queen bed" in text_lower:
            room_prefs["bed_type"] = "Queen"

        if "high floor" in text_lower or "upper floor" in text_lower:
            room_prefs["floor"] = "High"
        elif "low floor" in text_lower:
            room_prefs["floor"] = "Low"

        if "vegetarian" in text_lower:
            dietary.append("Vegetarian")
        if "vegan" in text_lower:
            dietary.append("Vegan")
        if "gluten free" in text_lower or "gluten-free" in text_lower:
            dietary.append("Gluten-Free")

        if "feather pillow" in text_lower:
            pillow = "Feather"
        elif "memory foam pillow" in text_lower or "foam pillow" in text_lower:
            pillow = "Memory Foam"

        # Apply updates if any detected
        if room_prefs or dietary or pillow:
            async with self.uow:
                guest = await self.uow.guests.get(str(guest_id))
                if not guest:
                    raise GuestNotFoundError(str(guest_id))

                prefs = guest.preferences or {}

                # Update room preferences
                existing_room = prefs.get("room_preferences", {})
                existing_room.update(room_prefs)
                prefs["room_preferences"] = existing_room

                # Update dietary restrictions
                existing_diet = set(prefs.get("dietary_restrictions", []))
                for item in dietary:
                    existing_diet.add(item)
                prefs["dietary_restrictions"] = list(existing_diet)

                # Update pillow preferences
                if pillow:
                    prefs["pillow_preferences"] = pillow

                guest.preferences = prefs
                await self.uow.commit()

                # Publish event
                await domain_event_publisher.publish(
                    PreferenceChanged(
                        guest_id=guest.id,
                        changed_preferences={
                            "room_preferences": str(prefs["room_preferences"]),
                            "dietary_restrictions": str(prefs["dietary_restrictions"]),
                            "pillow_preferences": str(prefs.get("pillow_preferences")),
                        },
                    )
                )
