# AI Platform: Structured Outputs

This document details Pydantic schema validation pipelines and corrective self-repair retry loops.

## Schema Validation Flow

```
[Prompt Completion Request]
           │
           ▼
     [LLM Response]
           │
           ▼
  [Structured Output Parser]
           ├── Is Valid JSON & matches Pydantic? ──► [Return Pydantic Object]
           │
           └── Parse/Validation Error?
                       │
                       ▼
             [Self-Repair Retry]
```

## Self-Repair Retries

On validation fail:
1. Append the invalid response content as an assistant message.
2. Append a user message detailing the exact validation error (e.g. `Field 'email' is missing`).
3. Request completion generation again from the LLM, prompting it to fix the JSON.
4. Retry up to 2 times before raising `ValidationError`.
