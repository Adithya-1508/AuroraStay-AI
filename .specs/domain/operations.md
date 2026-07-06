# Spec: Operations Domain Aggregates

- **Status**: Ready
- **Owner**: Operations Context Owner (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines the business rules, properties, and status lifecycles of housekeeping tasks and maintenance work orders.

## 2. Responsibilities
- Monitor room cleaning logs.
- Assign workers and track repair completion times.
- Auto-generate task queues on checkout events.

## 3. Public Interfaces
```python
class HousekeepingTask:
    def __init__(self, task_id: str, room_id: str):
        self.task_id = task_id
        self.room_id = room_id
        self.assigned_employee_id = None
        self.status = "Pending"

    def assign_to(self, employee_id: str) -> None:
        self.assigned_employee_id = employee_id
        self.status = "InProgress"

    def complete(self) -> None:
        if self.assigned_employee_id is None:
            raise ValueError("Task cannot be completed without an assignee.")
        self.status = "Complete"
```

## 4. Invariants
- Housekeeping tasks can only be created for rooms flagged as `Dirty` or `UnderMaintenance`.
- Complete tasks require an assignee ID.
