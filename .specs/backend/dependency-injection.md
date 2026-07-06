# Spec: Dependency Injection

- **Status**: Ready
- **Owner**: Backend Framework Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the dependency injection (DI) patterns, separating service logic from concrete database implementations.

## 2. Decoupled Service Boundary
- Services (e.g. `ReservationService`) must never initialize repositories directly.
- Repositories must inherit from abstract interface models (defined in `backend/repositories/`).
- Concrete repositories (database specific) are injected dynamically via FastAPI `Depends()`.

## 3. Dependency Injection Syntax
```python
# Conceptual DI wiring
def get_reservation_repository() -> AbstractReservationRepository:
    # Returns concrete repository implementation (SQLAlchemy, Qdrant, etc.)
    return SqlAlchemyReservationRepository()

@router.post("/reservations")
async def create_reservation(
    payload: ReservationCreate,
    repo: AbstractReservationRepository = Depends(get_reservation_repository)
):
    ...
```

## 4. Test Overrides
During unit testing runs, dependencies are overridden using standard fastapi client mechanisms:
```python
app.dependency_overrides[get_reservation_repository] = MockReservationRepository
```
