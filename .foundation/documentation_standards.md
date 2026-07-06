# Documentation Standards

Documentation is an integral part of the codebase. A feature is not complete until its documentation is complete and accurate.

## 1. Document Types and Locations
- **Architecture**: Stored under `docs/architecture/`.
- **System Specifications**: Stored under `.specs/`.
- **API Reference**: Generated automatically via FastAPI and documented in OpenAPI format.
- **Directories**: Every directory must contain a `README.md` explaining its purpose and ownership.

## 2. Python Docstring Standard
We use the **Google Python Style Guide** for docstrings. Every public module, class, and function must be documented:

```python
async def get_reservation(reservation_id: str) -> ReservationSchema:
    """Retrieves a reservation from the database.

    Args:
        reservation_id: The unique identifier of the reservation.

    Returns:
        ReservationSchema: The reservation details.

    Raises:
        ReservationNotFoundError: If no reservation matches the ID.
    """
```

## 3. Code-Doc Synchronization
- When modifying code that changes public behavior, database schemas, API routes, or environment configuration, the associated documentation **must** be updated in the same pull request.
- Outdated documentation is treated as a critical bug.

## 4. README structure
Every top-level directory `README.md` must contain:
1. **Purpose**: What responsibility this directory has.
2. **Ownership**: Which team or system module owns it.
3. **Architecture Context**: How it fits into the broader system.
4. **Key Interfaces**: Critical classes/methods exposed.
