# Agent Platform Architecture & Manuals

This directory contains the engineering manuals and architectural specifications of the HospitalityAI reusable multi-agent execution platform.

## Platform Layout

```
backend/
└── agents/
    ├── core/              # BaseAgent lifecycle hooks, registries, supervisor
    ├── planner/           # AgentPlanner goal decomposition engine
    ├── executor/          # AgentExecutor step runner calling dynamic tools
    ├── graph/             # WorkflowEngine compiling LangGraph state-graphs
    ├── checkpoints/       # BaseCheckpointer (Memory, PostgreSQL)
    └── telemetry/         # AgentTelemetryTracker metrics logs
```

## Documentation Manuals

- [agent-lifecycle.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/agents/agent-lifecycle.md)
- [planner.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/agents/planner.md)
- [workflow-engine.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/agents/workflow-engine.md)
- [state-management.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/agents/state-management.md)
- [supervisor.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/agents/supervisor.md)
- [checkpointing.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/agents/checkpointing.md)
- [telemetry.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/agents/telemetry.md)
