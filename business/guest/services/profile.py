import uuid
from typing import Any

from backend.models.guest import Guest
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.guest.domain.exceptions import GuestNotFoundError
from business.guest.domain.value_objects import ProfileDetails
from business.guest.events.publisher import domain_event_publisher
from business.guest.events.schemas import GuestProfileUpdated


class GuestProfileService:
    """Application service managing Guest Profiles and loyalty transitions."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def get_profile(self, guest_id: uuid.UUID) -> Guest:
        """Retrieves an active Guest profile using their unique ID."""
        async with self.uow:
            guest = await self.uow.guests.get(str(guest_id))
            if not guest:
                raise GuestNotFoundError(str(guest_id))
            return guest

    async def get_profile_by_email(self, email: str) -> Guest:
        """Retrieves an active Guest profile using their email address."""
        async with self.uow:
            guest = await self.uow.guests.get_by_email(email)
            if not guest:
                raise GuestNotFoundError(email)
            return guest

    async def create_profile(
        self, details: ProfileDetails, loyalty_tier: str = "Bronze"
    ) -> Guest:
        """Creates a new Guest profile and registers it in the persistence layer."""
        async with self.uow:
            # Check if email is already taken
            existing = await self.uow.guests.get_by_email(details.email)
            if existing:
                raise ValueError(f"Email '{details.email}' is already registered.")

            guest = Guest(
                first_name=details.first_name,
                last_name=details.last_name,
                email=details.email.strip().lower(),
                phone=details.phone,
                loyalty_tier=loyalty_tier,
                preferences={},
            )
            await self.uow.guests.add(guest)
            await self.uow.commit()
            return guest

    async def update_profile(
        self, guest_id: uuid.UUID, updates: dict[str, Any]
    ) -> Guest:
        """Updates fields on an existing Guest profile."""
        async with self.uow:
            guest = await self.uow.guests.get(str(guest_id))
            if not guest:
                raise GuestNotFoundError(str(guest_id))

            updated_fields = []
            for field_name, value in updates.items():
                if hasattr(guest, field_name) and field_name != "id":
                    setattr(guest, field_name, value)
                    updated_fields.append(field_name)

            if updated_fields:
                await self.uow.commit()
                # Publish profile updated event
                await domain_event_publisher.publish(
                    GuestProfileUpdated(
                        guest_id=guest.id,
                        updated_fields=updated_fields,
                    )
                )
            return guest
