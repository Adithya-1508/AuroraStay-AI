# AI Platform Architecture & Manuals

This directory contains the engineering manuals and architectural specifications of the HospitalityAI provider-agnostic AI Platform infrastructure.

## Platform Layout

```
backend/
└── ai/
    ├── providers/            # Adapters (NVIDIA NIM, Ollama, Mocks)
    ├── models/               # Model Registry tracking window sizes & pricing
    ├── routing/              # Model Router with failover chains logic
    ├── prompts/              # Prompts Registry loading template configs
    ├── structured_output/    # Schema validations and self-correcting parser
    ├── context/              # Token budget auditor and history trimmer
    ├── memory/               # Strategies (short-term, session-level memory)
    ├── tools/                # Declarative tool schemas and runtime execution
    ├── embeddings/           # Generic embedding client abstraction
    ├── cache/                # exact prompt hashing cache with TTL expiry
    ├── telemetry/            # Inference metrics and tracing logger
    ├── evaluation/           # Benchmarks runner comparing to golden datasets
    └── service.py            # AIService orchestrator facade
```

## Documentation Registry

- [provider-architecture.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/provider-architecture.md)
- [prompt-management.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/prompt-management.md)
- [model-routing.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/model-routing.md)
- [structured-output.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/structured-output.md)
- [tool-framework.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/tool-framework.md)
- [context-management.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/context-management.md)
- [memory-system.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/memory-system.md)
- [evaluation-framework.md](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/ai/evaluation-framework.md)
