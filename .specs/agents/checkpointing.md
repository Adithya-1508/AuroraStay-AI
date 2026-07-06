# Agent Specification: Checkpointing

This document describes checkpointing state snapshots and recoveries.

## Core Operations

- **Pause**: Intercepts step execution when encountering a `Human-in-the-loop` node. Saves current graph state and thread ID.
- **Resume**: Re-reads stored state by thread ID and continues execution from the interrupted node.
- **Rollback**: Reverts graph state to a previous node index checkpoint if validation fails.
- **Replay**: Re-runs a workflow path from previous inputs for test verification.
