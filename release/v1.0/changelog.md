# Changelog: HospitalityAI

All notable changes to this project are versioned below.

## [1.0.0] - 2026-07-17

### Added
- **Loop 17 Deployment Platform**: Modular OCI Terraform code, multi-stage Dockerfiles, Kubernetes manifests, Helm charts, backup scripts, and graceful shutdown handlers.
- **Loop 16 Security Platform**: JWT, hashed API keys, RBAC/ABAC controllers, PII encryption, audit trails, and incident tracking.
- **Loop 15 AIOps**: Prometheus metrics, structlog correlation IDs, PSI drift tracking, and incident dashboards.
- **Loop 14 Executive Platform**: Occupancy widget grids, AI-generated reports, and LangGraph assistants.
- **Loop 00-13 Foundations**: Core reservation schemas, priority upgrades allocation, stay pricing calculators, and Qdrant RAG retriever engines.

### Changed
- Refactored all API routers to mount under the central `/api/v1` gateway.
- Standardized ruff formats and strict Mypy static types across modules.
