# Docker Configurations Guide

This guide details our local container network and Dockerfile builds.

## 1. Container Ports Mappings

| Service | Host Port | Internal Port | Health Probing Method |
| --- | --- | --- | --- |
| **PostgreSQL** | 5432 | 5432 | `pg_isready -U postgres` |
| **Redis** | 6379 | 6379 | `redis-cli ping` |
| **Qdrant** | 6333 | 6333 | `curl http://localhost:6333/readyz` |
| **MinIO** | 9000 | 9000 | `curl http://localhost:9000/minio/health/live` |
| **MLflow** | 5000 | 5000 | `curl http://localhost:5000/` |

## 2. Rebuilding Dockerfiles
To rebuild python images (e.g. backend, worker) after updating packages in `pyproject.toml`:
```bash
docker compose build
```
These builds utilize multi-stage layers (Stage 1 uses `uv` to build virtualenvs; Stage 2 acts as a minimal slim runner).
