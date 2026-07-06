from enum import StrEnum


class ReservationStatus(StrEnum):
    REQUESTED = "Requested"
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CHECKED_IN = "CheckedIn"
    CHECKED_OUT = "CheckedOut"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


__all__ = ["ReservationStatus"]
