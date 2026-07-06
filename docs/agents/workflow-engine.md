# Agent Platform: Workflow Engine

This document describes how graphs compile and execute under LangGraph.

## State Transitions

We use a Compiled State Graph routing the following node stages:
- **`planner_node`**: Creates the plan and populates initial steps.
- **`executor_node`**: Executes current step index and validates approvals tags.
- **`human_approval_node`**: Pauses state thread if tool requires confirmation.
- **`supervisor_node`**: Validates checks, retry count limit boundaries, and success status flags.
