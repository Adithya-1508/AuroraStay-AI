# Dependency Rules & Clean Architecture Layers

HospitalityAI strictly enforces Clean Architecture. This document defines the responsibilities of each layer and the rules governing dependencies between them.

## 1. Architectural Layers

```
  ┌────────────────────────────────────────────────────────┐
  │                   Presentation Layer                   │
  │     (API Controllers, WebSockets, Serializer Schemas)   │
  └───────────────────────────┬────────────────────────────┘
                              │ Depends on
  ┌───────────────────────────▼────────────────────────────┐
  │                   Application Layer                    │
  │     (Use Case Services, Transactions, Event Triggers)   │
  └───────────────────────────┬────────────────────────────┘
                              │ Depends on
  ┌───────────────────────────▼────────────────────────────┐
  │                      Domain Layer                      │
  │     (Entities, Aggregates, Invariants, Interfaces)      │
  └────────────────────────────────────────────────────────┘
                              ▲
                              │ Implements
  ┌───────────────────────────┴────────────────────────────┐
  │                  Infrastructure Layer                  │
  │     (SQL Repositories, Redis Caches, HTTP Clients)     │
  └────────────────────────────────────────────────────────┘
```

---

## 2. Layer Responsibilities & Rules

### Domain Layer
- **Code Location**: `business/*/domain/`
- **Responsibilities**: Contains the business models (`Reservation`, `Room`, `Guest`), value objects, custom exceptions, and core domain services (like pricing logic).
- **Rule**: **No external dependencies**. The domain layer cannot import libraries like SQLAlchemy, FastAPI, or Pydantic. It must use raw Python classes and standard types.

### Application Layer
- **Code Location**: `business/*/application/`
- **Responsibilities**: Implements the use cases (e.g. `BookRoomUseCase`, `CancelStayUseCase`). Manages database transaction boundaries, checks system states, and publishes domain events.
- **Rule**: Depends *only* on the Domain layer. It communicates with infrastructure layers (like databases) through **Abstract Interfaces** (Repository Pattern).

### Presentation Layer
- **Code Location**: `api/`
- **Responsibilities**: Standardizes system access points. Expresses FastAPI routes, converts incoming HTTP JSON request bodies into Pydantic validation schemas, handles CORS, and intercepts JWT tokens.
- **Rule**: Depends only on the Application layer to execute use cases. **No business rules are allowed here**.

### Infrastructure Layer
- **Code Location**: `infrastructure/` & `database/`
- **Responsibilities**: Implements database interactions (SQLAlchemy sessions, Postgres configurations, Qdrant indexes), SMTP client integrations, MLflow calls, and Redis connections.
- **Rule**: Implements abstract interfaces declared in the Application or Domain layers. Classes are instantiated and wired into the application using **Dependency Injection** at startup (bootstrapped inside `backend/`).
