# Reliability Engineering & Graceful Shutdown

This document outlines the resilience patterns and graceful shutdown configurations.

## 1. Graceful Shutdown (SIGTERM)

To prevent dropped requests during pod rollouts:
1. Kubernetes sends a `SIGTERM` signal to the pod.
2. The ingress controller stops routing new requests.
3. The pod's graceful shutdown handler intercepts the signal and gives the application a 30-second window to complete in-flight transactions.
4. Active database connection pools and background threads are closed before the process exits.

## 2. Health Checks

- **Readiness Probes**: Query `/api/v1/deployment/readiness` to verify that external services (PostgreSQL, Redis, Qdrant) are reachable before routing traffic to the pod.
- **Liveness Probes**: Query `/api/v1/deployment/health` to reboot the container if a deadlock occurs.
