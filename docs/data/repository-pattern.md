# Data Platform: Repository Pattern & Unit of Work

This document details the abstract repository architecture and session-level transactional boundary layers.

## Repository Layers

1. **AbstractRepository[T]**:
   - Generic base interface declaring standard asynchronous CRUD methods:
     - `get(entity_id)`: retrieves active record by ID.
     - `get_all()`: retrieves list of active records.
     - `add(entity)`: queues new record insertion.
     - `update(entity)`: queues record update.
     - `delete(entity_id)`: marks record as logically deleted.
2. **PostgresRepository[T]**:
   - Concrete base implementation wrapping standard SQLAlchemy async queries and filters.
3. **Specialized Repositories**:
   - `GuestRepository`: Adds `get_by_email()`.
   - `ReservationRepository`: Adds `get_by_guest()`.
   - `ReviewRepository`: Adds `get_by_guest()`.

## Unit of Work (UoW) Pattern

Transactions are managed inside a Unit of Work class to ensure atomic changes:
- `PostgresUnitOfWork`:
  - `__aenter__`: Instantiates an async session and assigns active repositories linked to the session.
  - `commit()`: Executes session flush and commit operations.
  - `rollback()`: Executes transaction rollback.
  - `__aexit__`: Auto-rolls back modifications on exceptions and releases session resources back to the pool.
