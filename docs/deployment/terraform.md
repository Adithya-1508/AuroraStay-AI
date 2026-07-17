# Terraform Infrastructure as Code

This document outlines the OCI resources provisioned by the Terraform scripts.

## 1. Directory Structure

```
deployment/terraform/
├── main.tf           # Resource configurations (VCN, OKE, Object Storage)
├── variables.tf      # Variable declarations (OCIDs, regions, credentials)
└── outputs.tf        # Output variables (OKE endpoint, bucket names)
```

## 2. Resources Provisioned

- **OCI Identity Compartment**: Separates the Hospitality AI deployment workspace from other workloads.
- **OCI Virtual Cloud Network (VCN)**: Configures isolated subnets (Public and Private).
- **OCI Container Engine for Kubernetes (OKE)**: Provisions the managed Kubernetes API endpoint.
- **OCI Object Storage Buckets**:
  - `hospitality-knowledge-bucket`: Stores PDF, Markdown, and text document assets for RAG ingestion.
  - `hospitality-mlflow-bucket`: Stores ML model artifacts and metadata.

## 3. Provisioning Guidelines

To apply changes:
```bash
cd deployment/terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```
