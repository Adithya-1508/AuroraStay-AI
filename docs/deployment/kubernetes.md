# Kubernetes Platform Configuration

This document covers Kubernetes workload structures, persistence volumes, and routing rules.

## 1. Pod Deployment Schema

Stateless API instances run as standard deployments:
- **Replica Count**: 2 pods for high availability.
- **Auto-healing**: Probes monitor container health and restart failing pods automatically:
  - **Readiness Probe**: Queries `/api/v1/deployment/readiness` (drains traffic if database fails).
  - **Liveness Probe**: Queries `/api/v1/deployment/health` (reboots container if deadlocks occur).
- **Graceful termination**: Mapped `terminationGracePeriodSeconds: 30` to let active connection pools drain safely.

## 2. Stateful Services

Stateful storage configurations are managed as StatefulSets:
- **PostgreSQL**: Bound to dynamic persistent block volumes (`oci-bv` storage class).
- **Qdrant**: Manages collections indexes inside persistent volume claims.

## 3. Ingress Control

- **Service Access**: Core ingress rules map `/api` prefixes to backend services.
- **TLS Configuration**: Let's Encrypt certificates are stored inside `hospitality-tls-cert` secrets.
