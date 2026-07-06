# ADR-0006: Machine Learning Registry and Artifact Storage Selection

- **Status**: Approved
- **Date**: 2026-07-04
- **Author**: Antigravity AI Coding Agent
- **Owner**: ML Platform
- **Supersedes**: None

## Context
HospitalityAI runs custom forecasting and classification models (occupancy prediction, cancellation risks). These models must be trained, tracked for accuracy drifts, versioned, and easily loaded by inference services. Storing model binaries directly in git is a bad practice, and storing them randomly on the file system makes version tracking impossible.

## Decision
We select **MLflow** for tracking experiments and registering models, and **MinIO** as the S3-compatible backend storage for model binaries and artifacts.
- MLflow tracking server logs parameters and metrics (MAPE, F1-scores).
- Trained models are registered in the MLflow Model Registry.
- Model binaries and training datasets are stored as S3 objects in MinIO buckets.

## Rationale
- **Traceability**: MLflow tracks all model parameters and training metrics, enabling comparison of forecast performance across epochs.
- **Model Versioning**: The model registry allows us to tag model states (e.g. `Staging`, `Production`), ensuring the API gateway always loads the approved production variant.
- **MinIO S3 Abstraction**: MinIO acts as an offline, local S3 object store. This maintains provider independence by allowing us to use standard S3 SDKs, meaning we can swap local MinIO for AWS S3 in production with zero code changes.

## Alternatives Considered
- **Weights & Biases (WandB)**: Rejected. WandB is a proprietary SaaS product that does not fit the unified local containerization targets.
- **Raw File Pickles**: Saving `.pkl` files to a shared local directory was rejected as it lacks version control, experiment comparison, and model promotion pipelines.

## Consequences
- **Pros**:
  - Full audit trail of model parameters and forecasting metrics.
  - Decoupled, S3-compatible artifact storage.
- **Cons/Risks**:
  - Adds two containers (MLflow and MinIO) to our deployment stack.
- **Migration/Rollout**:
  - MLflow and MinIO services will be configured and verified in Loop 13 (Revenue Intelligence).
