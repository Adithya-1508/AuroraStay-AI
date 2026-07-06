# AI Platform: Provider Architecture

This document describes the provider abstraction layer design and response normalization rules.

## Core Design

The provider layer decouples downstream AI services from the concrete HTTP or client calls required by LLM providers:

```
[Business / Workflows]
        │
        ▼
   [AIService]
        │
        ▼
   [BaseProvider]
   ├── [NVIDIAProvider] ────► Integrate NVIDIA NIM REST completions
   ├── [OllamaProvider] ────► Local Ollama chat API completions
   └── [MockProvider]   ────► Returns preconfigured mock outputs
```

## Normalization Classes

1. **`ProviderResponse`**:
   - Standardizes completion outputs across providers:
     - `content`: Generated response text.
     - `tool_calls`: Mapped JSON structure of requested tool calls.
     - `usage`: Maps prompt, completion, and total token usage.
     - `model_name`: Mapped provider model key.
2. **`ProviderRegistry`**:
   - Indexes and caches instantiated provider singletons.
