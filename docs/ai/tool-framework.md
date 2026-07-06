# AI Platform: Tool Execution Framework

This document details tool mapping rules and runtime execution boundaries.

## BaseTool Specifications

Every tool registers:
- `name`: Unique key matching LLM mapping.
- `description`: Explains what the tool does to the model.
- `args_schema`: Pydantic BaseModel validating inputs.
- `permissions`: List of scopes (e.g. `write_reservations`).
- `timeout_sec`: Timeout limit (default 30s).
- `retries`: Execution retry limits.

## ToolExecutor Actions

1. Checks if caller scopes cover tool permissions, throwing `PermissionError` on failure.
2. Validates inputs using `args_schema`.
3. Runs execution wrapping `asyncio.wait_for` to enforce timeouts.
