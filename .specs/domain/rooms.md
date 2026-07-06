# Spec: Rooms Domain Aggregate

- **Status**: Ready
- **Owner**: Inventory Context Owner (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the properties, room category associations, and status lifecycles of individual hotel rooms.

## 2. Responsibilities
- Store room numbers, floor tags, and categories.
- Update cleaning states (Clean, Dirty, Under Maintenance).
- Prevent room check-ins if the room is not clean.

## 3. Public Interfaces
```python
class Room:
    def __init__(self, room_id: str, room_number: RoomNumber, category_id: str):
        self.room_id = room_id
        self.room_number = room_number
        self.category_id = category_id
        self.status = "Clean"

    def mark_dirty(self) -> None:
        self.status = "Dirty"

    def mark_clean(self) -> None:
        self.status = "Clean"

    def place_in_maintenance(self) -> None:
        self.status = "UnderMaintenance"
```

## 4. Invariants
- Room numbers must map to physical floors.
- A room cannot transition to `Occupied` if its status is `Dirty` or `UnderMaintenance`.
