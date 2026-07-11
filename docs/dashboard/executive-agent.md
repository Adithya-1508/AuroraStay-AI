# Executive Assistant Manual

## Overview
The Executive Assistant Agent is a compiled LangGraph state workflow that executes multi-node logical query resolution.

## Workflow DAG
```
START ──> [retrieve_metrics] ──> [retrieve_policy] ──> [reasoning] ──> END
```

## Interactions
- **POST** `/api/v1/dashboard/assistant`
  - **Body**: `{ "query": "Why is SLA low?" }`
  - **Output**: JSON payload including the generated text answer (`response`), resource `citations`, and `suggested_actions`.
- It uses the local `AIService` provider failover routing and reads relevant policy guidelines from the knowledge retriever index.
