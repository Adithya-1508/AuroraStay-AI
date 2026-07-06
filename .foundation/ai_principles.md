# AI Principles

These principles govern all AI and Large Language Model (LLM) interactions inside the HospitalityAI platform.

## 1. Provider and Model Abstraction
- Never call an LLM API directly from business logic. All interactions must pass through the `ai/` platform.
- Swapping LLM models (e.g., from Gemini to Claude, or GPT-4 to Llama) must require only configuration changes and adapter implementations, with zero modifications to the application layer.

## 2. Prompt Governance
- Prompts are codebase assets. They must be version-controlled, stored in designated template files, and never hardcoded in Python strings.
- Track prompt performance and versioning in tandem with system metrics.

## 3. Structured Input and Output
- **Deterministic Formats**: AI calls must use structured outputs (JSON Schemas or Pydantic models) wherever possible.
- **Validation**: Every AI output must be validated against a Pydantic model immediately after retrieval. Handle parsing errors gracefully by retrying or returning structured errors.

## 4. Agent Safety & Guardrails
- **Execution Limits**: All agent execution loops (e.g. LangGraph) must enforce maximum iteration limits (`max_concurrency` or `recursion_limit`) to prevent runaway loops and excessive API costs.
- **Tool Validation**: Validate all inputs passed to tools before execution.
- **Failures**: Implement fallback strategies (human-in-the-loop triggers, default answers, or human handoffs) for agent failures or ambiguities.
