from datetime import date
from decimal import Decimal
from typing import Any
from uuid import UUID

import structlog

from backend.models.reservation import Reservation
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.reservation.domain.enums import ReservationStatus
from business.reservation.domain.exceptions import (
    InvalidDateError,
    ReservationNotFoundError,
    RoomNotAvailableError,
    TransitionValidationError,
)
from business.reservation.domain.value_objects import BookingWindow
from business.reservation.events.publisher import domain_event_publisher
from business.reservation.events.schemas import (
    ReservationCheckedIn,
    ReservationCheckedOut,
    ReservationCompleted,
    ReservationConfirmed,
    ReservationCreated,
    ReservationUpdated,
)
from business.reservation.services.allocation import AllocationService
from business.reservation.services.availability import AvailabilityService
from business.reservation.services.history import ReservationHistoryService
from business.reservation.services.notification import notification_service
from business.reservation.services.pricing import PricingService

logger = structlog.get_logger()


class ReservationService:
    """Core Application Service coordinating reservation bookings, modifications, and check-ins."""

    def __init__(self) -> None:
        self.availability_service = AvailabilityService()
        self.pricing_service = PricingService()
        self.allocation_service = AllocationService()
        self.history_service = ReservationHistoryService()

    async def create_reservation(
        self,
        uow: AbstractUnitOfWork,
        guest_id: UUID,
        room_category_id: UUID,
        check_in_date: date,
        check_out_date: date,
        promo_code: str | None = None,
        preferences: dict[str, Any] | None = None,
    ) -> Reservation:
        """Validates stay intervals, verifies availability, computes cost, assigns room, and creates booking."""
        # 1. Validate booking window
        window = BookingWindow(
            check_in_date=check_in_date, check_out_date=check_out_date
        )
        if check_in_date < date.today():
            raise InvalidDateError("Check-in date cannot be in the past.")

        # 2. Verify availability
        available = await self.availability_service.check_category_availability(
            uow, room_category_id, window
        )
        if not available:
            raise RoomNotAvailableError(
                "Requested room category has no available rooms for the selected dates."
            )

        # 3. Get guest loyalty
        guest = await uow.guests.get(str(guest_id))
        loyalty_tier = guest.loyalty_tier if guest else "Bronze"

        # 4. Calculate pricing
        breakdown = await self.pricing_service.calculate_reservation_price(
            uow, str(room_category_id), window, loyalty_tier, promo_code
        )

        # 5. Create reservation record
        reservation = Reservation(
            guest_id=guest_id,
            room_category_id=room_category_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_cost=float(breakdown.total),
            status=ReservationStatus.PENDING,
        )
        await uow.reservations.add(reservation)
        await uow.session.flush()  # Flush to populate reservation.id

        # 6. Allocate Room
        assigned_room = None
        try:
            assigned_room = await self.allocation_service.allocate_room(
                uow, reservation.id, preferences
            )
            reservation.status = ReservationStatus.CONFIRMED
            await uow.reservations.update(reservation)
        except Exception as e:
            # Fallback: keep reservation as Pending if room allocation temporarily fails
            logger.debug("Room allocation failed, keeping as PENDING", error=str(e))

        # 7. Record History
        await self.history_service.record_transition(
            uow,
            reservation_id=reservation.id,
            old_status=None,
            new_status=reservation.status,
            changed_by="Guest",
            reason="Initial reservation request placement.",
        )

        # 8. Dispatch Domain Events
        created_event = ReservationCreated(
            reservation_id=reservation.id,
            guest_id=guest_id,
            room_category_id=room_category_id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            total_cost=breakdown.total,
        )
        await domain_event_publisher.publish(created_event)

        if reservation.status == ReservationStatus.CONFIRMED and assigned_room:
            confirmed_event = ReservationConfirmed(
                reservation_id=reservation.id,
                assigned_room_id=assigned_room.id,
            )
            await domain_event_publisher.publish(confirmed_event)

        # 9. Trigger Guest Notification
        if guest:
            category = await uow.room_categories.get(str(room_category_id))
            category_name = category.name if category else "Standard"

            details = {
                "reservation_id": str(reservation.id),
                "category_name": category_name,
                "check_in_date": str(check_in_date),
                "check_out_date": str(check_out_date),
                "total_cost": float(breakdown.total),
            }
            guest_name = f"{guest.first_name} {guest.last_name}"
            await notification_service.send_reservation_confirmation(
                guest_name=guest_name,
                guest_email=guest.email,
                guest_phone=guest.phone,
                reservation_details=details,
            )

        return reservation

    async def modify_reservation(
        self,
        uow: AbstractUnitOfWork,
        reservation_id: UUID,
        check_in_date: date | None = None,
        check_out_date: date | None = None,
        room_category_id: UUID | None = None,
        changed_by: str = "Guest",
    ) -> Reservation:
        """Alters booking dates/category, running collision checks and updating pricing billing."""
        # 1. Fetch reservation
        reservation = await uow.reservations.get(str(reservation_id))
        if not reservation:
            raise ReservationNotFoundError(f"Reservation '{reservation_id}' not found.")

        # 2. Check current status
        if reservation.status not in (
            ReservationStatus.PENDING,
            ReservationStatus.CONFIRMED,
        ):
            raise TransitionValidationError(
                f"Cannot modify a reservation in status '{reservation.status}'."
            )

        # 3. Identify modifications
        new_in = check_in_date or reservation.check_in_date
        new_out = check_out_date or reservation.check_out_date
        new_cat_id = room_category_id or reservation.room_category_id

        window = BookingWindow(check_in_date=new_in, check_out_date=new_out)
        if new_in < date.today() and new_in != reservation.check_in_date:
            raise InvalidDateError("Cannot modify check-in date to a past date.")

        old_dates = f"{reservation.check_in_date} to {reservation.check_out_date}"
        old_cost = Decimal(str(reservation.total_cost))

        # 4. Availability Check (Temporarily free own capacity during verification)
        original_status = reservation.status
        reservation.status = ReservationStatus.CANCELLED  # Mock cancel to free dates
        await uow.reservations.update(reservation)
        await uow.session.flush()

        try:
            available = await self.availability_service.check_category_availability(
                uow, new_cat_id, window
            )
            if not available:
                raise RoomNotAvailableError(
                    "Requested modification dates/category are not available."
                )
        finally:
            reservation.status = original_status
            await uow.reservations.update(reservation)
            await uow.session.flush()

        # 5. Pricing Re-calculation
        guest = await uow.guests.get(str(reservation.guest_id))
        loyalty_tier = guest.loyalty_tier if guest else "Bronze"
        breakdown = await self.pricing_service.calculate_reservation_price(
            uow, str(new_cat_id), window, loyalty_tier
        )

        # 6. Apply updates
        reservation.check_in_date = new_in
        reservation.check_out_date = new_out
        reservation.room_category_id = new_cat_id
        reservation.total_cost = float(breakdown.total)

        # Re-allocate Room since dates or category changed
        reservation.assigned_room_id = None
        await uow.reservations.update(reservation)
        await uow.session.flush()

        try:
            await self.allocation_service.allocate_room(uow, reservation.id)
            reservation.status = ReservationStatus.CONFIRMED
        except Exception as e:
            logger.debug(
                "Room reallocation failed, setting status to PENDING",
                error=str(e),
            )
            reservation.status = ReservationStatus.PENDING

        await uow.reservations.update(reservation)

        # 7. Record History
        await self.history_service.record_transition(
            uow,
            reservation_id=reservation.id,
            old_status=original_status,
            new_status=reservation.status,
            changed_by=changed_by,
            reason=f"Modified dates from {old_dates} to {new_in} - {new_out}.",
        )

        # 8. Event Publication
        updated_event = ReservationUpdated(
            reservation_id=reservation.id,
            old_check_in=reservation.check_in_date,  # Note: old dates before save can be fetched or passed
            new_check_in=new_in,
            old_check_out=reservation.check_out_date,
            new_check_out=new_out,
            old_total_cost=old_cost,
            new_total_cost=breakdown.total,
        )
        await domain_event_publisher.publish(updated_event)

        # 9. Notify Guest
        if guest:
            details = {
                "reservation_id": str(reservation.id),
                "check_in_date": str(new_in),
                "check_out_date": str(new_out),
                "total_cost": float(breakdown.total),
            }
            guest_name = f"{guest.first_name} {guest.last_name}"
            await notification_service.send_reservation_modification(
                guest_name=guest_name,
                guest_email=guest.email,
                guest_phone=guest.phone,
                reservation_details=details,
                old_dates=old_dates,
            )

        return reservation

    async def check_in(
        self, uow: AbstractUnitOfWork, reservation_id: UUID, changed_by: str = "Staff"
    ) -> Reservation:
        """Performs check-in, verifying room allocation and transitions state."""
        # 1. Fetch reservation
        reservation = await uow.reservations.get(str(reservation_id))
        if not reservation:
            raise ReservationNotFoundError(f"Reservation '{reservation_id}' not found.")

        # 2. Validate state transition
        if reservation.status != ReservationStatus.CONFIRMED:
            raise TransitionValidationError(
                f"Cannot check in reservation in status '{reservation.status}'. Must be Confirmed."
            )
        if not reservation.assigned_room_id:
            # Attempt to allocate room dynamically if missing
            await self.allocation_service.allocate_room(uow, reservation.id)
            await uow.session.flush()

        if not reservation.assigned_room_id:
            raise TransitionValidationError("Cannot check in without an assigned room.")

        old_status = reservation.status
        reservation.status = ReservationStatus.CHECKED_IN
        await uow.reservations.update(reservation)

        # Update physical room status to occupied or similar if needed
        room = await uow.rooms.get(str(reservation.assigned_room_id))
        if room:
            room.status = "Occupied"
            await uow.rooms.update(room)

        # 3. Record History
        await self.history_service.record_transition(
            uow,
            reservation_id=reservation_id,
            old_status=old_status,
            new_status=ReservationStatus.CHECKED_IN,
            changed_by=changed_by,
            reason="Guest checked in.",
        )

        # 4. Dispatch Event
        assert reservation.assigned_room_id is not None
        event = ReservationCheckedIn(
            reservation_id=reservation.id,
            assigned_room_id=reservation.assigned_room_id,
        )
        await domain_event_publisher.publish(event)

        # 5. Notify Guest
        guest = await uow.guests.get(str(reservation.guest_id))
        if guest and reservation.assigned_room_id:
            room = await uow.rooms.get(str(reservation.assigned_room_id))
            room_number = room.room_number if room else "Unknown"

            details = {
                "reservation_id": str(reservation.id),
                "room_number": room_number,
                "check_out_date": str(reservation.check_out_date),
            }
            guest_name = f"{guest.first_name} {guest.last_name}"
            await notification_service.send_check_in_confirmation(
                guest_name=guest_name,
                guest_email=guest.email,
                guest_phone=guest.phone,
                reservation_details=details,
            )

        return reservation

    async def check_out(
        self, uow: AbstractUnitOfWork, reservation_id: UUID, changed_by: str = "Staff"
    ) -> Reservation:
        """Processes check-out, releasing room allocations and billing completed status."""
        # 1. Fetch reservation
        reservation = await uow.reservations.get(str(reservation_id))
        if not reservation:
            raise ReservationNotFoundError(f"Reservation '{reservation_id}' not found.")

        # 2. Validate state transition
        if reservation.status != ReservationStatus.CHECKED_IN:
            raise TransitionValidationError(
                f"Cannot check out reservation in status '{reservation.status}'. Must be CheckedIn."
            )

        old_status = reservation.status
        reservation.status = ReservationStatus.CHECKED_OUT
        assigned_room_id = reservation.assigned_room_id

        # Update physical room status to Dirty (requiring housekeeping)
        if assigned_room_id:
            room = await uow.rooms.get(str(assigned_room_id))
            if room:
                room.status = "Dirty"
                await uow.rooms.update(room)

        # Release physical room linkage
        reservation.assigned_room_id = None
        await uow.reservations.update(reservation)

        # 3. Record History
        await self.history_service.record_transition(
            uow,
            reservation_id=reservation_id,
            old_status=old_status,
            new_status=ReservationStatus.CHECKED_OUT,
            changed_by=changed_by,
            reason="Guest checked out. Room released for housekeeping.",
        )

        # 4. Dispatch Event
        if assigned_room_id:
            event = ReservationCheckedOut(
                reservation_id=reservation.id, room_id=assigned_room_id
            )
            await domain_event_publisher.publish(event)

        # 5. Notify Guest
        guest = await uow.guests.get(str(reservation.guest_id))
        if guest:
            details = {
                "reservation_id": str(reservation.id),
                "check_out_date": str(reservation.check_out_date),
                "total_cost": float(reservation.total_cost),
            }
            guest_name = f"{guest.first_name} {guest.last_name}"
            await notification_service.send_check_out_confirmation(
                guest_name=guest_name,
                guest_email=guest.email,
                guest_phone=guest.phone,
                reservation_details=details,
            )

        return reservation

    async def complete_reservation(
        self, uow: AbstractUnitOfWork, reservation_id: UUID
    ) -> Reservation:
        """Archives and marks the checked out reservation stay as complete."""
        reservation = await uow.reservations.get(str(reservation_id))
        if not reservation:
            raise ReservationNotFoundError(f"Reservation '{reservation_id}' not found.")

        if reservation.status != ReservationStatus.CHECKED_OUT:
            raise TransitionValidationError(
                f"Cannot complete reservation in status '{reservation.status}'. Must be CheckedOut."
            )

        old_status = reservation.status
        reservation.status = ReservationStatus.COMPLETED
        await uow.reservations.update(reservation)

        await self.history_service.record_transition(
            uow,
            reservation_id=reservation_id,
            old_status=old_status,
            new_status=ReservationStatus.COMPLETED,
            changed_by="System",
            reason="Stay lifecycle completed.",
        )

        event = ReservationCompleted(reservation_id=reservation.id)
        await domain_event_publisher.publish(event)

        return reservation


__all__ = ["ReservationService"]
