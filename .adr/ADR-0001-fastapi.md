# ADR-0001: Programming Language and Web Framework Selection

- **Status**: Approved
- **Date**: 2026-07-04
- **Author**: Antigravity AI Coding Agent
- **Owner**: API Platform
- **Supersedes**: None

## Context
HospitalityAI requires an enterprise-ready, high-performance web backend. The system needs to support async database queries (PostgreSQL), high-volume concurrent chat sessions, vector search integrations, and ML inference workflows. It must also provide high developer velocity, strict type safety, and clean documentation capabilities.

## Decision
We choose **Python 3.12+** as the primary programming language and **FastAPI** as the core web framework.
- The backend will leverage Python's native `async/await` features.
- Pydantic v2 will be used for schema parsing, validations, and settings management.
- Uvicorn will act as the ASGI server.

## Rationale
- **Performance**: FastAPI is one of the fastest Python frameworks available, approaching Node.js and Go performance levels due to its Starlette-based async core.
- **Developer Experience**: Auto-generates interactive Swagger and ReDoc API specifications, reducing documentation drift.
- **Type Safety**: Native type-hinting support integrates cleanly with mypy, Ruff, and Black, aligning with [Coding Standards](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.foundation/coding_standards.md).
- **ML Integration**: The ML/AI ecosystem is predominantly Python-based. Choosing Python avoids polyglot complexity (e.g. Node backend talking to Python ML scripts).

## Alternatives Considered
- **Django (Django REST Framework)**: Reverted due to its synchronous legacy ORM structure. While Django 4+ supports async, it is not async-first, and features like middlewares and ORM are still largely synchronous.
- **Node.js (Express/NestJS)**: Rejected. NestJS provides robust structure but forces a multi-language setup (Node for APIs, Python for ML/AI models), increasing dependency footprints and build complexity.

## Consequences
- **Pros**:
  - High async throughput.
  - Native Pydantic validation.
  - Clean API contract interfaces.
- **Cons/Risks**:
  - Developers must write strict async code to prevent blocking the event loop.
- **Migration/Rollout**:
  - Python 3.12 and FastAPI will be bootstrapped in Loop 04.
