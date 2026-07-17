# Runbook: Deployment Rollback Process

This runbook guides administrators through reverting a release to the previous stable revision.

## 1. Prerequisites

- Installed `helm` CLI.
- Access to the target Kubernetes cluster.

## 2. Automated Rollback

If a deployment fails, the CI/CD pipeline triggers an automatic rollback:
```bash
helm rollback hospitality-ai -n hospitality
```

## 3. Manual Rollback

If production bugs are discovered post-release:
1. **Identify Previous Revision**:
   ```bash
   helm history hospitality-ai -n hospitality
   ```
2. **Execute Rollback**:
   ```bash
   helm rollback hospitality-ai [PREVIOUS_REVISION_NUMBER] -n hospitality
   ```
3. **Verify Rollback Status**:
   ```bash
   kubectl rollout status deployment/backend-api -n hospitality
   ```
