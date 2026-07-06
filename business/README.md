# Business Layer Directory

## Purpose
The Core Domain and Application Layer. This directory houses the business domain logic, aggregates, entities, and services. Business modules must remain fully decoupled from each other and use repository patterns to hide database engines.

## Ownership
- **Owner**: Domain Engineering Team (Antigravity AI Coding Agent)
- **Primary Domain**: Business Rules, Invariants, Transactions, Domain Events

## Planned Business Modules
- `reservations/`: Core reservation and booking logic.
- `guests/`: Guest profiles, preferences, and details.
- `operations/`: Housekeeping, task allocation, and maintenance.
- `revenue/`: Occupancy intelligence and dynamic pricing rules.
- `reviews/`: Guest reviews and sentiment aggregation.
