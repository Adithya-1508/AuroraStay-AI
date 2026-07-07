from datetime import date, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ReservationBaseEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1


class ReservationCreated(ReservationBaseEvent):
    reservation_id: UUID
    guest_id: UUID
    room_category_id: UUID
    check_in_date: date
    check_out_date: date
    total_cost: Decimal


class ReservationUpdated(ReservationBaseEvent):
    reservation_id: UUID
    old_check_in: date
    new_check_in: date
    old_check_out: date
    new_check_out: date
    old_total_cost: Decimal
    new_total_cost: Decimal


class ReservationCancelled(ReservationBaseEvent):
    reservation_id: UUID
    reason: str
    penalty_applied: Decimal = Decimal("0.0")


class ReservationConfirmed(ReservationBaseEvent):
    reservation_id: UUID
    assigned_room_id: UUID


class ReservationCheckedIn(ReservationBaseEvent):
    reservation_id: UUID
    assigned_room_id: UUID


class ReservationCheckedOut(ReservationBaseEvent):
    reservation_id: UUID
    room_id: UUID


class ReservationCompleted(ReservationBaseEvent):
    reservation_id: UUID


__all__ = [
    "ReservationBaseEvent",
    "ReservationCreated",
    "ReservationUpdated",
    "ReservationCancelled",
    "ReservationConfirmed",
    "ReservationCheckedIn",
    "ReservationCheckedOut",
    "ReservationCompleted",
]
