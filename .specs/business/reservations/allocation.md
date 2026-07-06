# Spec: Room Allocation Engine

- **Status**: Draft
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-06

## 1. Purpose
Define the algorithm for assigning a specific room number to a reservation.

## 2. Responsibilities
- Assign a physical room to a reservation from the requested category.
- Apply priority upgrade logic for high-tier loyalty guests when requested category is sold out.
- Satisfy room preferences (e.g. low floor, quiet room, temp settings) during allocation.

## 3. Dependencies
- **Data Platform**: To retrieve room inventory, categories, status, and active allocations.

## 4. Interfaces
```python
class AllocationEngine:
    async def allocate_room(
        self, reservation_id: UUID, preferences: Optional[dict] = None
    ) -> Room:
        """Assigns the best available room to the reservation, applying priority upgrades if needed."""
        pass

    async def release_room_allocation(self, reservation_id: UUID) -> None:
        """Clears room assignment link."""
        pass
```

### Upgrade Priority Order
If a category is overbooked or sold out, check available upgrades:
1. Platinum loyalty tier guests are processed first.
2. Gold loyalty tier guests next.
3. Order by reservation date (first booker gets priority).

## 5. Configuration
- `AUTO_UPGRADE_ALLOWED`: Default True.
- `UPGRADE_MAX_TIERS`: Default 1 tier (e.g., Standard can upgrade to Deluxe, but not directly to Suite unless Deluxe is also sold out).

## 6. Error Handling
- `AllocationConflictError`: Raised if double room allocation is attempted.
- `InventoryExhaustedError`: Raised if no rooms or eligible upgrade paths are available.

## 7. Security
- Room allocations can only be overridden by Staff or Manager profiles.

## 8. Testing
- **Unit Tests**:
  - Test loyalty-based upgrade selection.
  - Test preferences matching (e.g., matching a pillow type preference).
- **Integration Tests**:
  - Assert concurrent allocation requests handle locks properly and prevent assigning the same physical room.

## 9. Acceptance Criteria
- [ ] Physical rooms are assigned without conflicts.
- [ ] High loyalty guests receive priority upgrades when category is sold out.
- [ ] Room preferences are respected where feasible.
