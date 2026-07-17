# Future Product Roadmap: Version 2.0.0

This document outlines upcoming product capabilities and architecture targets planned for HospitalityAI Version 2.0.0.

## 1. Planned Capabilities

- **Autonomous Agent Negotiations**: Allow AI agents to dynamically negotiate pricing and package offers directly with guests based on historical occupancy.
- **Multilingual Support**: Expand agent conversational graphs to support multi-language RAG ingestion (Arabic, Spanish, French, etc.).
- **Real-Time SMS integrations**: Connect Twilio gateways directly to agent routing nodes.

## 2. Infrastructure & Operations Roadmap

- **Canary Deployments**: Automate traffic split routing (e.g. 90/10) using Service Mesh (Istio/Linkerd) configurations.
- **Multi-Region Databases**: Active-active PostgreSQL replica databases across multiple cloud provider geographical zones.
- **Dynamic Autoscaling Extensions**: Integrate Kubernetes Event-driven Autoscaling (KEDA) utilizing custom queue metrics.
