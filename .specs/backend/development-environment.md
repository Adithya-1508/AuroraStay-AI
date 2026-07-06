# Spec: Local Development Environment

- **Status**: Ready
- **Owner**: DevOps Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define ports, services, and health probes for local containers.

## 2. Ports Assignments
- PostgreSQL: `5432`
- Redis: `6379`
- Qdrant: `6333`
- MinIO: `9000` / `9001`
- MLflow: `5000`
- Prometheus: `9090`
- Grafana: `3000`

## 3. Health check mandates
All database and storage services must declare active compose health checks, blocking application startup until databases are ready.
