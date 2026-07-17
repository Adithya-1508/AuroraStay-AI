# Workloads Scaling & Resource Sizing

This document covers auto-scaling logic and resource limits.

## 1. Horizontal Scaling (HPA)

Workloads auto-scale dynamically based on CPU and memory limits:
- **`backend-api`**:
  - Auto-scales when average CPU exceeds 75% or memory exceeds 80%.
  - Min: 2 replicas, Max: 10 replicas.
- **`worker-agent`**:
  - Auto-scales when average CPU exceeds 80% or memory exceeds 85%.
  - Min: 2 replicas, Max: 8 replicas.

## 2. Resource Constraints

Workloads define requests and limits to ensure efficient CPU scheduling:
- **Requests**: Represents the minimum resources guaranteed to a container (e.g. CPU 250m, Memory 256Mi).
- **Limits**: Represents the maximum resources a container can consume (e.g. CPU 1000m, Memory 512Mi).
