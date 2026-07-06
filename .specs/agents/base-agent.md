# Agent Specification: Base Agent Lifecycle

This document describes the abstract Base Agent lifecycle hooks and states.

## Lifecycle States

An agent transition follows these states:
`UNINITIALIZED` -> `INITIALIZING` -> `READY` -> `PLANNING` -> `EXECUTING` -> `VALIDATING` -> `FINALIZING` -> `TERMINATED`.

If an error occurs, it transitions to `RECOVERING` or `FAILED`.

## Lifecycle Hooks

Every agent subclass must support the following asynchronous methods:

- `async def initialize(self) -> None`: Prepares context and resources.
- `async def plan(self, goal: str) -> ExecutionPlan`: Decomposes goal into steps.
- `async def execute(self, plan: ExecutionPlan) -> ExecutionResult`: Performs execution.
- `async def validate(self, result: ExecutionResult) -> bool`: Checks outputs integrity.
- `async def finalize(self) -> None`: Saves state and clears temporary caches.
- `async def recover(self, error: Exception) -> bool`: Attempts state recovery.
- `async def shutdown(self) -> None`: Closes background resources.
