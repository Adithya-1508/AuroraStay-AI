# Domain Decision Log

This document records the architectural and domain design choices made during the modeling phase of HospitalityAI.

---

## Decision 1: Embed Stay Lifecycle within Reservation
- **Date**: 2026-07-04
- **Status**: Approved
- **Context**: We debated whether to create a separate `Stay` aggregate or represent stays within the `Reservation` aggregate.
- **Decision**: Stays are modeled as state changes and attributes inside the `Reservation` aggregate.
- **Rationale**: Stays are a phase in a reservation's lifecycle. Maintaining a separate `Stay` aggregate would introduce synchronization complexity and database redundancy.

---

## Decision 2: Keep Humans in the Loop for VIP Upgrades
- **Date**: 2026-07-04
- **Status**: Approved (Modified by User)
- **Context**: Determine if VIP room upgrades should be processed automatically by system triggers.
- **Decision**: The system will generate a `Recommendation` for staff review, which must be approved to execute.
- **Rationale**: Keeps front desk managers in control of room assignments, preventing automated double allocation conflicts or inventory shortfalls.

---

## Decision 3: Model Decision as a Separate Aggregate
- **Date**: 2026-07-04
- **Status**: Approved
- **Context**: Tracks pricing adjustments or upgrades.
- **Decision**: Modeled `Decision` as an independent aggregate linked to a unique `Recommendation` ID.
- **Rationale**: Enforces a strict audit trail, documenting who approved a price change or room upgrade, when, and the associated reason.
