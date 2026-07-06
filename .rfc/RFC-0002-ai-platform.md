# RFC-0002: AI Platform and Multi-Agent Orchestration Design

- **Author**: Antigravity AI Coding Agent
- **Status**: Draft
- **Date**: 2026-07-04
- **Target Release/Loop**: Loop 07 — Loop 08

## 1. Summary
This RFC proposes the detailed workflow logic of the AI Platform and the multi-agent graph (LangGraph) setup.

## 2. Proposed Design

### Conversational Gateway & Adapters
We propose an abstract `LlmAdapter` interface that handles provider calls. Individual adapters (e.g. `GeminiAdapter`, `ClaudeAdapter`) will translate requests into provider-specific payloads. This ensures we can easily swap LLM models with zero impact on the agent code.

### Agent Stateful Graph Layout
We define the LangGraph state model to track the conversational state:
- **Router (Supervisor)**: Evaluates incoming messages and routes them to sub-agents (e.g., FAQ Agent, Reservation Agent).
- **FAQ Node**: Executes vector retrieval, builds prompts, and returns answers.
- **Reservation Planner Node**: Receives booking requests, decomposes actions, and executes tools.
- **Validator Node**: Runs post-generation validation checks on output schemas.

```
Guest Message ──► Supervisor Router ──┬──► FAQ Agent (RAG) ──────► Output
                                      └──► Reservation Agent ───► Output
```

## 3. Testing and Verification
- Run agent simulation runs on mock FAQs, validating that the router successfully flags handoffs and checks recursion thresholds.
