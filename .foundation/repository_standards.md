# Repository Standards

This document establishes the repository structure, directory responsibilities, and file naming conventions.

## 1. Directory Structure and Responsibilities

HospitalityAI is organized into specialized directories. No directory may exceed its defined scope:

- `.adr/`: Architecture Decision Records.
- `.foundation/`: Global governance rules and principles.
- `.loops/`: Iterative specifications and plans for Loop Engineering.
- `.prd/`: Product Requirements Documents.
- `.rfc/`: Request For Comments documents.
- `.specs/`: Canonical implementation specifications.
- `.templates/`: Reusable templates for ADRs, RFCs, and specs.
- `agents/`: AI agents built with LangGraph.
- `ai/`: Foundation LLM interfaces and provider adapters.
- `api/`: API controllers, routing, schemas, and gateway.
- `backend/`: Application server infrastructure.
- `business/`: Isolated domain business modules (reservations, housekeeping, etc.).
- `dashboard/`: Frontend visualization and UI code.
- `database/`: Database migrations, seeds, and schema files.
- `deployment/`: Docker, Docker-compose, and cloud configuration files.
- `docs/`: System documentation and architecture diagrams.
- `etl/`: Data extraction, cleaning, and ingestion pipelines.
- `infrastructure/`: Connectors for external systems (e.g. database adapters, caches).
- `knowledge-platform/`: RAG pipelines, chunking, and vector searches.
- `ml/`: Custom model training, inference, and registries.
- `observability/`: Logs, metrics, and traces configuration.
- `rag/`: Core index and retrieval logic.
- `shared/`: Shared models, schemas, and helper utils.
- `testing/`: End-to-end and system integration tests.

## 2. Naming Conventions
- **Directories**: Use `kebab-case` (e.g., `knowledge-platform`).
- **Python Files & Modules**: Use `snake_case` (e.g., `reservation_service.py`).
- **Classes**: Use `PascalCase` (e.g., `ReservationService`).
- **Variables & Functions**: Use `snake_case` (e.g., `get_reservation_by_id`).
- **Constants**: Use `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_COUNT`).
- **Tests**: Prefix test files with `test_` and test methods with `test_`.

## 3. Module Layout
Each Python package must contain an `__init__.py` file exposing only its public interface. Avoid exposing internal helper classes or files.
