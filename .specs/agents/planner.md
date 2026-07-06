# Agent Specification: Planner

This document describes the Planner engine responsible for task decomposition.

## Plan Representation

An `ExecutionPlan` contains a directed acyclic graph (DAG) of steps:
- `plan_id`: Unique UUID.
- `steps`: List of steps.
- `dependencies`: Maps a step ID to a list of step IDs that must run first.

## Plan Step Schema

```json
{
  "step_id": "step_1",
  "name": "fetch_guest_history",
  "tool": "get_guest",
  "arguments": {
    "guest_id": 101
  },
  "status": "PENDING"
}
```
