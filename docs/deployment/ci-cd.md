# CI/CD Pipelines & Automation

This document outlines the Continuous Integration (CI) and Continuous Deployment (CD) pipeline automation workflows.

## 1. Continuous Integration (CI)

Every code push and PR submission triggers the CI runner:
1. **Code Hygiene**: Format code with `ruff format --check` and lint with `ruff check`.
2. **Type Checking**: Runs `mypy --explicit-package-bases` to ensure type annotations are valid.
3. **Unit & Integration Tests**: Executes `pytest` with code coverage reports (`--cov`).
4. **Security Analysis**: Evaluates Python scripts with `bandit` and scans build images with `trivy`.
5. **Artifact Build**: Compiles multi-stage production Docker images and publishes to OCI Artifact Registry.

## 2. Continuous Deployment (CD)

Upon merging changes into the `main` branch:
1. **Build & Package**: Creates container images tagged with the commit SHA and semantic version.
2. **Deploy to Dev**: Deploys services to the Dev Kubernetes namespace with HPA disabled.
3. **Smoke Tests**: Verifies API endpoints return valid JSON metadata.
4. **Deploy to Staging**: Promotes images to Staging environment.
5. **Approval Gate**: Pauses pipeline execution. Admins must explicitly review and click approve.
6. **Deploy to Production**: Performs a rolling update across active Production Pods.
