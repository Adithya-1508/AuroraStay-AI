from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from backend.models.reservation import ReservationHistory
from backend.repositories.unit_of_work import AbstractUnitOfWork


class ReservationHistoryService:
    """Application Service auditing reservation lifecycle changes."""

    async def record_transition(
        self,
        uow: AbstractUnitOfWork,
        reservation_id: UUID,
        old_status: str | None,
        new_status: str,
        changed_by: str | None = "System",
        reason: str | None = None,
    ) -> ReservationHistory:
        """Saves a status change event into the audit trail database table."""
        history_entry = ReservationHistory(
            reservation_id=reservation_id,
            old_status=old_status,
            new_status=new_status,
            changed_by=changed_by,
            reason=reason,
        )
        await uow.reservation_histories.add(history_entry)
        return history_entry

    async def get_history_by_reservation(
        self, uow: AbstractUnitOfWork, reservation_id: UUID
    ) -> Sequence[ReservationHistory]:
        """Retrieves complete audit trail entries for a booking."""
        stmt = (
            select(ReservationHistory)
            .filter_by(reservation_id=reservation_id, is_deleted=False)
            .order_by(ReservationHistory.timestamp.asc())
        )
        result = await uow.session.execute(stmt)
        res_seq: Sequence[ReservationHistory] = result.scalars().all()
        return res_seq


__all__ = ["ReservationHistoryService"]
