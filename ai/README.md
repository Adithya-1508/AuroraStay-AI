# AI Platform Directory

## Purpose
This directory houses the foundational LLM client interfaces, prompt management, and safety guardrails. It ensures the platform remains provider-agnostic by exposing generic adapters for models (e.g. Gemini, Claude, Llama, OpenAI) and managing prompt version control.

## Ownership
- **Owner**: AI Platform Team (Antigravity AI Coding Agent)
- **Primary Domain**: LLM Gateways, Prompt Templates, Model Adapters, Content Moderation

## Key Responsibilities
1. Abstraction of LLM provider integrations via adapters.
2. Structured output parsing and output schema validation.
3. System guardrails (max tokens, input/output validation, pricing/latency logging).
