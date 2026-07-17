# Runbook: Standard Deployment & Verification

This runbook guides administrators through standard rolling updates and deployment checks.

## 1. Prerequisites

- Access to the target OKE Kubernetes cluster via `kubectl`.
- Installed `helm` CLI tool.
- Valid deployment credentials configured.

## 2. Execution Steps

1. **Deploy Helm Release**:
   ```bash
   helm upgrade --install hospitality-ai ./deployment/helm/hospitality-ai \
     -f ./deployment/environments/production/values-prod.yaml \
     --namespace hospitality --create-namespace
   ```
2. **Track Deployment Progress**:
   ```bash
   kubectl rollout status deployment/backend-api -n hospitality
   ```

## 3. Post-Deployment Verification

1. **Verify API Status**:
   ```bash
   curl -f http://hospitalityai.local/api/v1/deployment/status
   ```
2. **Verify Database Connections**:
   ```bash
   curl -f http://hospitalityai.local/api/v1/deployment/health
   ```
If status check is not healthy, trigger the rollback runbook immediately.
