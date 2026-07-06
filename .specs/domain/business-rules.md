# Spec: Domain Business Rules

- **Status**: Ready
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the business rules evaluation interfaces, detailing constraints and exception scopes.

## 2. Responsibilities
- Evaluate overlap conflicts.
- Evaluate room category suitability.
- Enforce check-in constraints.

## 3. Public Interfaces
```python
class ReservationRulesChecker:
    @staticmethod
    def assert_no_overlap(target_range: DateRange, active_bookings: List[DateRange]) -> None:
        """Raises overlap exception if target date overlaps with active bookings list."""
        for active in active_bookings:
            if target_range.overlaps(active):
                raise ValueError("Dates overlap with active reservation.")
```
