# OCI Production Cloud Architecture

This document outlines the target cloud reference architecture utilizing Oracle Cloud Infrastructure (OCI).

## 1. Network Topology (VCN)

The platform is deployed inside a Virtual Cloud Network (VCN) mapped to `10.0.0.0/16` CIDR.

- **VCN CIDR**: `10.0.0.0/16`
- **Subnet Configuration**:
  - **Public Subnet (`10.0.1.0/24`)**: Hosts OCI Load Balancers, API gateways, and public-facing OKE API endpoints.
  - **Private Worker Subnet (`10.0.2.0/24`)**: Hosts Kubernetes cluster node pool compute workers (no direct public ingress).
  - **Private Database Subnet (`10.0.3.0/24`)**: Hosts Autonomous Databases and transactional storage structures.

## 2. Gateways & Routing

- **Internet Gateway**: Mapped to Public Subnet for load balancing ingress and outbound public responses.
- **NAT Gateway**: Mapped to Private Worker Subnet to allow compute nodes to pull images and resolve external API calls (e.g. OpenAI/NVIDIA API).
- **Service Gateway**: Establishes secure connections from worker subnet to OCI Object Storage bucket.

## 3. Compute Engine & Clusters (OKE)

- **OCI Container Engine for Kubernetes (OKE)**: Managed cluster running active Kubernetes version `1.30+`.
- **Node Pool Shapes**: Managed OCI VM instances running ARM Ampere `VM.Standard.A1.Flex` shapes.
- **Boot Storage**: 50 GB block volumes per node.
