# Spec: Domain Events

- **Status**: Ready
- **Owner**: Shared Domain Infrastructure (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Defines the base structure and specifications for all core Domain Events.

## 2. Responsibilities
- Standardize event metadata fields.
- Track event publisher identities.

## 3. Public Interfaces
```python
class DomainEvent:
    def __init__(self, event_id: str, publisher: str):
        self.event_id = event_id
        self.publisher = publisher
        self.timestamp = datetime.utcnow()
```

## 4. Sub-Event Catalog Specifications
Detailed schemas for events (e.g. `ReservationCreated`, `GuestCheckedIn`, `HousekeepingTaskCreated`) are mapped as subclasses of the base `DomainEvent` class, containing details specific to their target context.
