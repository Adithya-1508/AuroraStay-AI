# ADR-0002: Relational Database and Architecture Patterns Selection

- **Status**: Approved
- **Date**: 2026-07-04
- **Author**: Antigravity AI Coding Agent
- **Owner**: Data Platform & Domain Engineering
- **Supersedes**: None

## Context
HospitalityAI's core operations require strict transactional integrity. Room reservations, checkout logs, and housekeeper task allocations cannot suffer from data drift or race conditions. Additionally, the codebase must remain highly maintainable, allowing developers to refactor database schemas or models without impacting core business rules.

## Decision
We select **PostgreSQL** as our primary relational database, **SQLAlchemy 2.x** (async-style) as our Object-Relational Mapper (ORM), and enforce **Clean Architecture** combined with **Domain-Driven Design (DDD)** patterns.
- Business entities, invariants, and aggregate boundaries are declared in the Domain layer with zero dependencies.
- Application use cases delegate database tasks to Repository Interfaces.
- SQLAlchemy mappings and async sessions are implemented in the Infrastructure layer.

## Rationale
- **Transactional Integrity (ACID)**: Reservations require strict isolation to prevent overbookings. PostgreSQL provides industry-standard ACID guarantees and robust concurrency control.
- **Relational Fit**: Reservations, rooms, guests, and cleaning tasks are highly structured and naturally relate, making relational tables a perfect fit.
- **Clean Architecture & Repository Pattern**: Separating database entities from business models prevents the domain logic from becoming tightly coupled to SQLAlchemy schemas, enabling easy database migrations.

## Alternatives Considered
- **MongoDB**: Rejected. NoSQL does not naturally support the multi-table transactions required for room booking schedules and availability checks without complex application-level enforcement.
- **Direct ORM Coupling**: Directly exposing ORM entities in API controllers (Active Record pattern) was rejected to comply with the constitution's [Rule 7](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.foundation/execution-rules.md) and prevent database changes from breaking API structures.

## Consequences
- **Pros**:
  - Eliminates overbooking race conditions via SQL transaction boundaries.
  - Ensures the Domain layer can be fully tested without database mocks.
- **Cons/Risks**:
  - Overhead from mapping data between ORM entities and domain models.
- **Migration/Rollout**:
  - PostgreSQL schema and SQLAlchemy configurations will be implemented in Loop 06.
