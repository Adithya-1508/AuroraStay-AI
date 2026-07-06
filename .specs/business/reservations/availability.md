# Spec: Availability Engine

- **Status**: Draft
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-06

## 1. Purpose
Define the availability check mechanisms, overlap mathematics, and alternative suggestions logic.

## 2. Responsibilities
- Identify which rooms and room categories are available for a given `BookingWindow` and guest preferences.
- Perform high-performance date overlap math to prevent double bookings.
- Suggest alternative dates or alternative room types when the requested booking window is fully occupied.

## 3. Dependencies
- **Data Platform**: Read-only queries for active bookings and room tables.

## 4. Interfaces
```python
class AvailabilityEngine:
    async def check_category_availability(
        self, category_id: UUID, window: BookingWindow
    ) -> bool:
        """Returns True if at least one room in category is unreserved during window."""
        pass

    async def get_available_rooms(
        self, window: BookingWindow, preferences: Optional[dict] = None
    ) -> List[Room]:
        """Lists specific room objects available during date range."""
        pass

    async def suggest_alternatives(
        self, requested_category_id: UUID, window: BookingWindow
    ) -> List[AlternativeOption]:
        """Generates alternative dates or categories if requested window is unavailable."""
        pass
```

### Overlap Math Formula
Let a requested interval be $[S_{req}, E_{req})$ and an existing booking interval be $[S_{exist}, E_{exist})$. A collision occurs if:
$$S_{req} < E_{exist} \quad \text{and} \quad E_{req} > S_{exist}$$

## 5. Configuration
- `MAX_ALTERNATIVE_SUGGESTIONS`: Default 3 alternatives.
- `SEARCH_WINDOW_EXTENSION_DAYS`: Default 7 days forward and backward for alternative dates.

## 6. Error Handling
- `NoAvailabilityError`: Raised when check fails and no alternatives are found.

## 7. Security
- Public search allowed, but detailed room inventories and histories restricted to Staff roles.

## 8. Testing
- **Unit Tests**:
  - Test extensive boundary conditions for date overlaps (adjacent, nested, partial overlap, outer overlap).
- **Integration Tests**:
  - Verify that database query filters for overlaps execute correctly and run within performance benchmarks (< 50ms).

## 9. Acceptance Criteria
- [ ] No room can have overlapping active reservations on any night.
- [ ] Alternative dates are correctly suggested when the original selection is unavailable.
- [ ] Supports filtering by category and specific amenities/preferences.
