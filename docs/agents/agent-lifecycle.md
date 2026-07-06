# Agent Platform: Agent Lifecycle

This document describes the lifecycle stages, transitions, and callbacks for agents.

## Lifecycle States

```
[UNINITIALIZED] ──► [INITIALIZING] ──► [READY] ◄─── (recovery success)
                                         │
                                         ▼
                                     [PLANNING]
                                         │
                                         ▼
                                    [EXECUTING]
                                         │
                                         ├─── (on error) ──► [RECOVERING]
                                         ▼                         │
                                    [VALIDATING]                   ├─── (recovery fail)
                                         │                         ▼
                                         ▼                     [FAILED]
                                    [FINALIZING]
                                         │
                                         ▼
                                   [TERMINATED]
```

## Abstract Callbacks

- `_on_initialize`: Custom setup actions.
- `_on_plan`: Goal decomposition routines.
- `_on_execute`: Executes plan steps.
- `_on_validate`: Output evaluations.
- `_on_recover`: Custom recovery rules.
- `_on_shutdown`: Releases resources.
