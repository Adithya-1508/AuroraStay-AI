# Agent Specification: Workflow Engine

This document details LangGraph engine construction rules.

## Core Node Graph

```
       [Start]
          │
          ▼
      [Planner]
          │
          ▼
      [Executor] ◄─── retry?
          │
          ├─── (Conditional Branching)
          ▼
    [Human Input?] (Interrupt Node)
          │
          ▼
     [Supervisor] ◄─── recover?
          │
          ▼
        [End]
```

## Graph Rules

1. Graph state is represented by a centralized `AgentState` Dict.
2. Nodes represent processing stages: Planning, Execution, Verification, and Pauses.
3. Edge transitions are determined by state fields (`next_step`, `error`, `paused`).
