# Spec: Reservations Domain Aggregate

- **Status**: Ready
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the business rules, state transitions, and properties of the `Reservation` aggregate.

## 2. Responsibilities
- Track stay dates and night rate aggregates.
- Prevent overlapping room assignments.
- Calculate costs based on seasonal pricing rules.
- Manage check-in, check-out, and cancellation flows.

## 3. Public Interfaces
```python
# Pure domain entities. No SQLAlchemy or Pydantic.

class Reservation:
    def __init__(self, reservation_id: str, guest_id: str, date_range: DateRange, room_category_id: str):
        self.reservation_id = reservation_id
        self.guest_id = guest_id
        self.date_range = date_range
        self.room_category_id = room_category_id
        self.assigned_room_id = None
        self.status = "Confirmed"
        self.total_cost = Money(0, "USD")

    def assign_room(self, room: Room) -> None:
        if room.status != "Clean":
            raise ValueError("Cannot assign a dirty or out-of-order room.")
        self.assigned_room_id = room.room_id

    def check_in(self) -> None:
        if self.status != "Confirmed":
            raise ValueError("Can only check in confirmed reservations.")
        self.status = "CheckedIn"

    def check_out(self) -> None:
        if self.status != "CheckedIn":
            raise ValueError("Can only check out active stays.")
        self.status = "CheckedOut"

    def cancel(self) -> None:
        if self.status != "Confirmed":
            raise ValueError("Cannot cancel check-ins or completed stays.")
        self.status = "Cancelled"
```

## 4. Invariants
- `check_out` date must be after `check_in` date.
- Stays cannot exceed 30 consecutive nights.

## 5. Security & Validation
- Validate that the guest exists before confirming a reservation.
- Date ranges cannot be in the past at reservation creation.
