# Spec: Container Deployment & Orchestration

- **Status**: Ready
- **Owner**: Infrastructure & Operations Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the containerization standards, docker networks, volume mount locations, environment settings, and compose configurations for development, staging, and production environments.

## 2. Responsibilities
- Containerize the API Backend and Background Worker.
- Standardize multi-container orchestration via `docker-compose.yml`.
- Standardize service dependency boot sequences using explicit container health checks.
- Manage persistent volumes for database directories (Postgres, Qdrant, MinIO).

## 3. Dependencies
- **Docker**: Containerization engine.
- **Docker Compose v2**: Multi-container coordinator.

## 4. Public Interfaces
- No code interfaces. Expressed via:
  - `Dockerfile`: Standardized python build.
  - `docker-compose.yml`: Local multi-service config.
  - `healthcheck` scripts.

## 5. Configuration
- `DOCKER_NETWORK_NAME`: Internal network name (default: `hospitality_net`).
- `VOLUME_MAPPINGS`: Persistence bounds:
  - `postgres_data` -> `/var/lib/postgresql/data`
  - `qdrant_data` -> `/qdrant/storage`
  - `minio_data` -> `/data`
  - `mlflow_data` -> `/mlflow`

## 6. Failure Modes
- **Orchestration Crash**: If an infrastructure container (e.g. Redis) crashes, Docker compose is configured with `restart: unless-stopped` to automatically reboot the process.
- **Port Conflict**: If port conflicts occur locally, developers can override configurations using a `.env` file mapping external ports.

## 7. Security Considerations
- Run containers as non-root users where possible.
- Bind external database ports (`5432`, `6333`, `6379`) only to `127.0.0.1` locally to block external access.
- Exclude `.env` files from version control.

## 8. Testing Strategy
- **Orchestration Tests**: Test the compose startup sequence on a clean machine to verify health checks, service dependencies, and storage volume creation.
- **Build Checks**: Run CI pipeline tests verifying that the Dockerfile builds successfully with zero errors.
