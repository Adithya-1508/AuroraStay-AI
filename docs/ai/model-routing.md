# AI Platform: Model Registry & Router

This document details the registry schemas and routing failover policies.

## Model Metadata Schema

The registry caches model parameters:
- `name`: Mapped provider key name.
- `provider`: NVIDIA, Ollama, Mock, etc.
- `context_window`: Maximum input window.
- `input_cost_per_1k`, `output_cost_per_1k`: Financial rates.
- `supports_tools`, `supports_streaming`: Capabilities.

## Model Selector Policies

The `ModelRouter` maps incoming tasks to models dynamically:
- `planning` task -> routes to high-capability `nvidia/meta/llama3-70b-instruct`.
- `summarization` task -> routes to local `ollama/llama3`.
- General fallback -> routes to settings-configured `DEFAULT_MODEL`.

## Failover Policy

When a provider request fails:
- Router evaluates the next fallback provider (e.g. `nvidia` -> `ollama` -> `mock`).
- Selects the fallback provider's mapped model and triggers retry, tracking retry count in telemetry.
