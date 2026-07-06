# Agent Specification: Executor

This document details execution steps processing and dynamic tool invocations.

## Execution Rules

1. Loops through ready plan steps (those whose dependencies are resolved).
2. Maps step `tool` key to registered `BaseTool` instances inside the tool framework.
3. Invokes the tool asynchronously.
4. Updates step execution status: `RUNNING` -> `SUCCESS` or `FAILED`.
5. Retries failed steps up to step-configured limit using exponential backoff.
