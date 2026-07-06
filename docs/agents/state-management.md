# Agent Platform: State Management

This document tracks graph execution state mapping fields.

## Graph State Dictionary

State fields tracked in every run thread:
- `thread_id`: Unique identifier tracking the conversation context session.
- `goal`: User prompt input target.
- `tools`: Target tools list.
- `plan_steps`: List of steps.
- `completed_steps`: Completed step IDs.
- `current_step_idx`: Step index pointer.
- `paused`, `requires_approval`, `approval_given`: Human-in-the-loop flags.
- `step_results`: Logged inputs/outputs.
- `success`: Execution outcome.
