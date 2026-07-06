# Agent Specification: Supervisor

This document outlines supervision logic and unrecoverable error escalations.

## Supervision Tasks

- **Heartbeat & Status Checks**: Periodically checks running step durations to detect hung tasks.
- **Recovery Manager**: Triggers agent `recover()` hook on failure.
- **Escalation Rules**: If recovery fails or step retry counts exceed limits, halts execution, marks workflow as `FAILED`, and escalates to human operator via state checkpoints.
