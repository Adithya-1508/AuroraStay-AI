# Local Development Instructions

This document guides developers on launching databases, checking status, and running tests.

## 1. Running Local Infrastructure
HospitalityAI requires local databases and event servers running. Start these containers via Docker Compose:
```bash
docker compose up -d
```
This boots PostgreSQL, Redis, Qdrant, MinIO, MLflow, Prometheus, and Grafana.

## 2. Infrastructure Health Checks
Verify that all services are online and answering on their expected ports using the health check script:
```bash
python scripts/healthcheck.py
```

## 3. Running Verification Suites
- **Linting & Formatting**:
  ```bash
  ruff check .
  ruff format --check .
  ```
- **Type Checking**:
  ```bash
  mypy shared tests
  ```
- **Unit & Integration Tests**:
  ```bash
  pytest
  ```
