# Third-Party Dependency Matrix

This document maps all external libraries and package versions used in HospitalityAI.

## 1. Core Python Packages

| Package Name | Target Version | Category / Purpose |
|---|---|---|
| `fastapi` | `^0.110.0` | API Routing & Gateway |
| `uvicorn` | `^0.28.0` | ASGI Web Server |
| `sqlalchemy` | `^2.0.28` | Async ORM Database access |
| `asyncpg` | `^0.29.0` | PostgreSQL async driver |
| `qdrant-client`| `^1.8.0` | Vector Database queries |
| `mlflow` | `^2.11.3` | Model experiment tracking |
| `structlog` | `^24.1.0` | JSON telemetry logging |
| `pyjwt[crypto]`| `^2.8.0` | JWT tokens authorization |
| `cryptography` | `^42.0.5` | Field-level encryption service |
| `pydantic` | `^2.6.4` | Schemas and configurations |

## 2. Dev & Test Libraries

- **`pytest`**: Testing framework.
- **`pytest-cov`**: Pytest plugin for code coverage reports.
- **`ruff`**: Code formatter and linter.
- **`mypy`**: Static type checker.
