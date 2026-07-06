# Spec: Reservation Domain Model and Lifecycle

- **Status**: Draft
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-06

## 1. Purpose
Define the schema, state transitions, validation, and lifecycle invariants for the `Reservation` domain entity and its components.

## 2. Responsibilities
- Manage reservation details (dates, guest association, room assignments, pricing totals).
- Enforce lifecycle state transition boundaries.
- Track audit trail records using `ReservationHistory`.

## 3. Dependencies
- **Data Platform**: For persistence using SQLAlchemy models.
- **Guest / Room Domains**: For validating guest profiles and room category availability.

## 4. Interfaces
```python
class ReservationStatus(str, Enum):
    REQUESTED = "Requested"
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CHECKED_IN = "CheckedIn"
    CHECKED_OUT = "CheckedOut"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class BookingWindow(BaseModel):
    check_in_date: date
    check_out_date: date

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingWindow":
        if self.check_in_date < date.today():
            raise ValueError("Check-in date cannot be in the past.")
        if self.check_out_date <= self.check_in_date:
            raise ValueError("Check-out date must be after check-in.")
        return self
```

### Lifecycle Invariants
The valid state transitions are:
1. `Requested` -> `Pending` (awaiting payment/room assignment)
2. `Pending` -> `Confirmed` (payment received and room allocated)
3. `Confirmed` -> `CheckedIn` (guest checks in)
4. `CheckedIn` -> `CheckedOut` (guest checks out)
5. `CheckedOut` -> `Completed` (archival/billing closed)
6. `Requested` / `Pending` / `Confirmed` -> `Cancelled` (cancellation policy checks)

Invalid transitions (e.g. `Cancelled` -> `CheckedIn`, `Completed` -> `Cancelled`) must raise a `TransitionValidationError`.

## 5. Configuration
- `MIN_STAY_DAYS`: Default 1 night.
- `MAX_STAY_DAYS`: Default 30 nights.

## 6. Error Handling
- `TransitionValidationError`: Raised when violating state machine rules.
- `BookingWindowValidationError`: Raised when invalid date spans are supplied.

## 7. Security
- Read operations allowed for authenticated Guest (own bookings) and Staff.
- Create/modify operations audited and checked against JWT user identity claims.

## 8. Testing
- **Unit Tests**:
  - Test all valid and invalid state transitions.
  - Assert date boundary checks (e.g., check-in today vs yesterday).
- **Integration Tests**:
  - Test SQL storage and retrieval of the enum and history records.

## 9. Acceptance Criteria
- [ ] Only valid lifecycle state transitions are permitted.
- [ ] History records are automatically generated on every transition.
- [ ] Booking window validations prevent historical stays.
