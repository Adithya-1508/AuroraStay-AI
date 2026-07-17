# Production Engineering, Cloud Deployment & Platform Reliability

This directory contains system documentation for cloud provisioning, deployments automation, and reliability engineering on Oracle Cloud Infrastructure (OCI).

## Platform Architecture

```mermaid
graph TD
    User[End User] -->|HTTPS| LoadBalancer[OCI Load Balancer]
    LoadBalancer -->|Port 443| Ingress[NGINX Ingress Controller]
    
    subgraph OKE [OCI Container Engine for Kubernetes]
        Ingress -->|Route /api| Backend[Backend API Pods]
        Ingress -->|Route /| Dashboard[Dashboard Streamlit Pods]
        Backend -->|Schedule Job| Worker[Background Worker Pods]
    end

    Backend -->|Read/Write| Postgres[(PostgreSQL DB System)]
    Backend -->|Read/Write| Redis[(Redis Cache Pod)]
    Backend -->|Query Vectors| Qdrant[(Qdrant Vector DB Pod)]
    Backend -->|Log Metrics| Prometheus[(Prometheus Monitoring)]
    Prometheus -->|Fetch Dashboard| Grafana[(Grafana Console)]
    
    Backend -->|Save Run| MLflow[MLflow Server Pod]
    MLflow -->|Archive Run| ObjectStorage[OCI Object Storage Bucket]
```

## Deployment Reference Files

1. **[Production Cloud Architecture](production-architecture.md)**: High-level design separating networks, subnets, and compute.
2. **[CI/CD Pipelines Documentation](ci-cd.md)**: Git-driven integration checks, security container scans, and promotion stages.
3. **[Kubernetes Container Orchestration](kubernetes.md)**: Specifications of Pod manifests, liveness/readiness indicators, and persistent storages.
4. **[Terraform Infrastructure as Code](terraform.md)**: Declarative OCI resource configurations.
5. **[Release Management & Rollback](release-process.md)**: Semantic versioning, blue-green upgrades, and automatic triggers.
6. **[Database & State Backups](backup-recovery.md)**: pg_dump scripts, Qdrant snapshots, and object bucket synchronizations.
7. **[Workloads Scaling & Resources](scaling.md)**: Configured limits and metrics governing HPAs.
8. **[Service Reliability & Graceful Exit](reliability.md)**: Graceful shutdown timeouts and SIGTERM event handling.
