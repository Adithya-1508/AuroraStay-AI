# Spec: Reservations Business Domain

- **Status**: Ready
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the business rules, invariants, and workflows for checking room availability, creating new guest reservations, modifying existing booking schedules, and managing cancellations.

## 2. Responsibilities
- Validate stay intervals (e.g. check-in date must be in the future, and check-out must be after check-in).
- Prevent room overbooking by checking calendar date overlaps.
- Calculate reservation rates based on room type, stay duration, and configured seasonal pricing constants.
- Lock room inventory temporarily during check-out flow to avoid double bookings.
- Track room status transitions (e.g. Clean, Dirty, Out of Order).

## 3. Dependencies
- **Data Platform**: For persisting guest details, bookings history, and room definitions.
- **Shared Utils**: For standard schemas, exception formatting, and ID generators.

## 4. Interfaces
```python
# Conceptual interfaces for Reservation Service

class ReservationService:
    async def search_availability(
        self, check_in: date, check_out: date, room_type_id: str
    ) -> List[RoomSchema]:
        """Returns available rooms that do not overlap with active bookings."""
        pass

    async def create_reservation(
        self, guest_id: str, room_type_id: str, check_in: date, check_out: date
    ) -> ReservationSchema:
        """Locks inventory, calculates total cost, and creates a booking record."""
        pass

    async def modify_reservation(
        self, reservation_id: str, check_in: date, check_out: date, room_type_id: Optional[str] = None
    ) -> ReservationSchema:
        """Alters dates of an active booking, verifying room availability."""
        pass

    async def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancels booking, clears room lock, and logs events."""
        pass
```

## 5. Configuration
- `BASE_ROOM_RATES`: Dictionary mapping room types (Single, Double, Deluxe, Suite) to base nightly costs.
- `SEASONAL_PRICE_MULTIPLIERS`: Multipliers applied for weekend stays or peak seasons.

## 6. Error Handling
- `InvalidDateError`: Raised when check-out is before check-in or stay dates are historical.
- `RoomNotAvailableError`: Raised when a booking request overlaps with an existing reservation.
- `ReservationNotFoundError`: Raised when attempting to modify or cancel a non-existent reservation ID.

## 7. Security
- Guests can view, modify, or cancel only their own reservations (enforced by JWT sub checks).
- Staff and Managers can search and alter any reservation.
- Database access must use parameters to block SQL injection.

## 8. Testing
- **Unit Tests**:
  - Verify stay date overlap math (testing boundary dates like side-by-side stays, duplicate spans).
  - Verify pricing math with weekend and holiday multipliers.
- **Integration Tests**:
  - Test concurrent booking calls to ensure race conditions do not lead to double bookings.

## 9. Acceptance Criteria
- [ ] Prevents duplicate room allocations on identical nights.
- [ ] Recalculates reservation pricing accurately when dates or room types are modified.
- [ ] Releases rooms instantly back into availability pools when booking is cancelled.
