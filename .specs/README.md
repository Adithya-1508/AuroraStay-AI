# System Specifications (.specs/)

This directory houses the canonical implementation specifications for all components of the HospitalityAI platform. Every feature, database modification, API route, or agent model must have a corresponding specification before implementation begins.

## Specification Directory Map

- **`business/`**: Specifications for core domain entities and business rules (e.g. reservation, guest).
- **`backend/`**: Specifications for application-wide infrastructure, servers, pipelines, and frameworks.
- **`database/`**: Database schemas, columns, indexes, and relationship definitions.
- **`agents/`**: Specifications for AI agents, multi-agent frameworks, supervisors, and planners.
- **`ai/`**: Specifications for prompt templates, adapters, model gateways, and guardrails.

## Specification Rules
1. A specification must be written and approved before implementation begins ([Definition of Ready](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.foundation/definition_of_ready.md)).
2. Each specification should use the [Specification Template](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/.templates/specification.md).
3. Update specifications immediately when changes are made during implementation.
