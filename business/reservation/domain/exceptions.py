class ReservationDomainError(Exception):
    """Base exception class for all reservation domain errors."""

    pass


class InvalidDateError(ReservationDomainError):
    """Raised when stay dates are invalid or historically in the past."""

    pass


class RoomNotAvailableError(ReservationDomainError):
    """Raised when the requested room category or room is occupied during check-in/out range."""

    pass


class ReservationNotFoundError(ReservationDomainError):
    """Raised when the requested reservation ID cannot be located."""

    pass


class TransitionValidationError(ReservationDomainError):
    """Raised when violating the reservation state machine lifecycle rules."""

    pass


class AllocationConflictError(ReservationDomainError):
    """Raised when double room allocation is attempted on a physical room."""

    pass


class InventoryExhaustedError(ReservationDomainError):
    """Raised when no rooms or upgrades are available."""

    pass


__all__ = [
    "ReservationDomainError",
    "InvalidDateError",
    "RoomNotAvailableError",
    "ReservationNotFoundError",
    "TransitionValidationError",
    "AllocationConflictError",
    "InventoryExhaustedError",
]
