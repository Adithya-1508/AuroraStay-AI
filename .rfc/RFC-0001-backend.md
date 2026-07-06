# RFC-0001: Backend Platform Design

- **Author**: Antigravity AI Coding Agent
- **Status**: Draft
- **Date**: 2026-07-04
- **Target Release/Loop**: Loop 04 — Loop 06

## 1. Summary
This RFC proposes the concrete structural design of the HospitalityAI backend, defining the routing patterns, SQLAlchemy async sessions, and dependency injection container structures.

## 2. Proposed Design

### Directory Structure
To support Clean Architecture, we partition the backend code into isolated modules:
```
backend/
├── app.py             # Startup factory
├── config.py          # Settings loader
├── container.py       # Dependency injector
└── middleware/        # Global request filters
```

### Async Database Session Middleware
Each incoming request obtains an isolated SQLAlchemy database session context, which is committed at endpoint completion and automatically rolled back if an unhandled exception occurs:
```python
async def db_session_middleware(request: Request, call_next):
    async with db_session_factory() as session:
        request.state.db = session
        try:
            response = await call_next(request)
            await session.commit()
            return response
        except Exception as e:
            await session.rollback()
            raise e
```

### Dependency Injection
We will use a lightweight DI container (e.g. `dependency-injector` or a custom helper) to resolve interface dependencies at runtime. This ensures we can easily swap adapters (e.g. mock repositories in test suites).

## 3. Testing and Verification
- Run local unit tests checking that the transaction middleware rolls back correctly when routes throw exceptions.
