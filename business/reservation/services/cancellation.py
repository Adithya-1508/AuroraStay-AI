from datetime import date
from decimal import Decimal
from uuid import UUID

from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.reservation.domain.enums import ReservationStatus
from business.reservation.domain.exceptions import (
    ReservationNotFoundError,
    TransitionValidationError,
)
from business.reservation.events.publisher import domain_event_publisher
from business.reservation.events.schemas import ReservationCancelled
from business.reservation.services.history import ReservationHistoryService
from business.reservation.services.notification import notification_service


class CancellationService:
    """Orchestrates cancellation transactions, calculating penalties and releasing resources."""

    def __init__(self) -> None:
        self.history_service = ReservationHistoryService()

    async def cancel_reservation(
        self,
        uow: AbstractUnitOfWork,
        reservation_id: UUID,
        reason: str,
        cancelled_by: str | None = "Guest",
    ) -> Decimal:
        """Cancels booking, checks pre-arrival dates for penalties, and dispatches events."""
        # 1. Fetch reservation
        reservation = await uow.reservations.get(str(reservation_id))
        if not reservation:
            raise ReservationNotFoundError(f"Reservation '{reservation_id}' not found.")

        # 2. Check current status validation
        old_status = reservation.status
        if old_status in (
            ReservationStatus.CANCELLED,
            ReservationStatus.CHECKED_OUT,
            ReservationStatus.COMPLETED,
        ):
            raise TransitionValidationError(
                f"Cannot cancel a reservation in state '{old_status}'."
            )

        # 3. Fetch room category nightly rate
        category = await uow.room_categories.get(str(reservation.room_category_id))
        base_rate = Decimal(str(category.base_price)) if category else Decimal("0.0")

        # 4. Check policy (penalty if check-in is < 24 hours away)
        today = date.today()
        days_to_checkin = (reservation.check_in_date - today).days
        penalty = Decimal("0.0")
        if days_to_checkin < 1:
            penalty = base_rate

        # 5. Perform cancellation updates
        reservation.status = ReservationStatus.CANCELLED
        reservation.assigned_room_id = None  # Release allocation
        await uow.reservations.update(reservation)

        # 6. Audit Trail
        await self.history_service.record_transition(
            uow,
            reservation_id=reservation_id,
            old_status=old_status,
            new_status=ReservationStatus.CANCELLED,
            changed_by=cancelled_by,
            reason=reason,
        )

        # 7. Notify Guest
        guest = await uow.guests.get(str(reservation.guest_id))
        if guest:
            details = {
                "reservation_id": str(reservation.id),
                "penalty": float(penalty),
            }
            guest_name = f"{guest.first_name} {guest.last_name}"
            await notification_service.send_reservation_cancellation(
                guest_name=guest_name,
                guest_email=guest.email,
                guest_phone=guest.phone,
                reservation_details=details,
                reason=reason,
            )

        # 8. Domain Event
        event = ReservationCancelled(
            reservation_id=reservation.id,
            reason=reason,
            penalty_applied=penalty,
        )
        await domain_event_publisher.publish(event)

        return penalty


__all__ = ["CancellationService"]
