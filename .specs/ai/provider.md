# AI Platform Specification: LLM Provider Layer

## Overview
Defines a unified, provider-agnostic interface to normalize communications between backend services and LLM providers.

## Abstractions
- `BaseProvider` abstract base class defining core methods:
  - `generate(prompt, options) -> ProviderResponse`
  - `generate_stream(prompt, options) -> AsyncIterator[ProviderResponse]`
  - `embed(texts) -> list[list[float]]`

## Normalization Schemes
- Input: Messages standard representation `[{"role": "system" | "user" | "assistant", "content": str, "tool_calls": list}]`.
- Output: `ProviderResponse` dataclass/model:
  - `content`: Text response string.
  - `tool_calls`: Standardized list of requested tool invocations `[{"id": str, "name": str, "arguments": dict}]`.
  - `usage`: Dict tracking `prompt_tokens`, `completion_tokens`, and `total_tokens`.
  - `model_name`: Mapped provider model key.

## Concrete Adapters
1. **NVIDIA NIM Adapter**: Calls NVIDIA's inference services endpoints.
2. **Ollama Adapter**: Connects to localhost API for local execution.
3. **Mock Provider**: Returns pre-defined static answers or echoes input variables for testing.
