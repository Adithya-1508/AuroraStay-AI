# Runbook: TLS Certificate Rotation

This runbook guides administrators through rotating Let's Encrypt TLS certificates manually.

## 1. Prerequisites

- Installed `cert-manager` inside the OKE Kubernetes cluster.
- Configured OCI DNS credentials.

## 2. Rotation Verification

Certificates are rotated automatically by `cert-manager` every 60 days. To trigger a manual renewal:

1. **Locate Certificate Resource**:
   ```bash
   kubectl get certificate -n hospitality
   ```
2. **Trigger Manual Rotation**:
   ```bash
   kubectl cert-manager renew hospitality-tls-cert -n hospitality
   ```
3. **Verify Generation Status**:
   ```bash
   kubectl describe certificate hospitality-tls-cert -n hospitality
   ```
   Confirm Status is marked as `Ready` and `valid: true`.
4. **Reload Ingress Controller**:
   Force NGINX Ingress controller reload:
   ```bash
   kubectl rollout restart deployment/ingress-nginx-controller -n ingress-nginx
   ```
