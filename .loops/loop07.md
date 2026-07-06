LOOP 07 — AI Platform (LLM Infrastructure & Provider Abstraction)

Version: 1.0

Project: HospitalityAI

Status: Mandatory

Prerequisites

Loop 00 — Constitution
Loop 01 — Product Requirements
Loop 02 — Architecture
Loop 03 — Domain Modeling
Loop 04 — Repository Bootstrap
Loop 05 — Backend Core Platform
Loop 06 — Data Platform
Purpose

Build the AI infrastructure that powers every intelligent capability in HospitalityAI.

This loop does NOT build AI agents.

Instead, it builds the reusable AI platform that agents, workflows, and business modules consume.

The AI Platform should be provider-agnostic, observable, configurable, testable, and production-ready.

Philosophy

The AI Platform is an infrastructure layer—not a business layer.

Business modules should never call an LLM directly.

Instead, they should interact with the AI Platform through clean interfaces.

Objectives

Develop a centralized AI Platform capable of:

Managing LLM providers
Routing model requests
Versioning prompts
Executing tool calls
Managing context windows
Handling structured outputs
Supporting provider failover
Logging AI interactions
Measuring token usage
Enabling evaluation
Deliverables

Create the following structure:

backend/

ai/
│
├── providers/
│   ├── base.py
│   ├── nvidia.py
│   ├── ollama.py
│   ├── mock.py
│   └── registry.py
│
├── prompts/
│   ├── templates/
│   ├── registry.py
│   ├── versioning.py
│   └── validator.py
│
├── models/
│
├── context/
│
├── routing/
│
├── tools/
│
├── memory/
│
├── evaluation/
│
├── telemetry/
│
├── cache/
│
├── structured_output/
│
├── embeddings/
│
└── orchestration/
AI Platform Components

The platform should consist of the following major components.

Provider Layer

Responsibilities

Connect to LLM providers
Normalize responses
Retry requests
Handle rate limits
Support streaming
Expose unified interface

Supported providers

NVIDIA NIM
Ollama
Mock Provider

Future providers

OpenAI
Anthropic
Azure OpenAI

Business code must never know which provider is being used.

Model Registry

Maintain metadata for every available model.

Track:

Model Name
Provider
Capabilities
Context Window
Input Cost
Output Cost
Max Tokens
Streaming Support
Tool Calling Support

The registry should allow model selection without changing application code.

Model Router

Create an intelligent routing layer.

Example responsibilities:

Choose model based on task
Select cheapest compatible model
Handle provider fallback
Support configurable routing policies

Routing should be configurable rather than hardcoded.

Prompt Management

Prompts are first-class assets.

Every prompt must include:

Name
Version
Description
Owner
Variables
Output Schema
Test Cases

Store prompts separately from application logic.

Never embed long prompts inside Python files.

Structured Output

Support deterministic AI responses.

Implement:

JSON schema validation
Typed output parsing
Retry on invalid responses
Error reporting

Prefer structured outputs over free-form text whenever possible.

Context Management

Design a reusable context system.

Responsibilities:

Conversation history
Token budgeting
Context trimming
Session management
Metadata injection

The context manager should prevent context window overflow.

Memory Layer

Support multiple memory strategies.

Examples:

Conversation memory
Session memory
Long-term memory (placeholder)
Working memory

Memory implementations should be interchangeable.

Tool Framework

Create a generic tool execution framework.

Every tool must declare:

Name
Description
Input Schema
Output Schema
Permissions
Timeout
Retry Policy

The framework should support future LangGraph agents.

Embedding Layer

Provide a unified interface for embeddings.

Responsibilities:

Generate embeddings
Batch embedding
Version embeddings
Cache embeddings

No vector database logic yet.

That belongs to Loop 09.

AI Cache

Implement semantic caching.

Cache:

Prompt hash
Response
Model
Provider
Timestamp

Support configurable expiration policies.

AI Telemetry

Track every inference.

Metrics:

Latency
Token Usage
Prompt Version
Model Used
Provider
Success Rate
Failure Reason
Retry Count
AI Evaluation

Create evaluation framework.

Support:

Golden datasets
Prompt regression
Output comparison
Structured evaluation
Human review workflow

The framework should support future automated benchmarking.

Configuration

Support:

MODEL_PROVIDER

DEFAULT_MODEL

EMBEDDING_MODEL

TEMPERATURE

MAX_TOKENS

TIMEOUT

CACHE_ENABLED

STREAMING_ENABLED

No hardcoded model names.

APIs

Do not expose public AI business endpoints.

Only internal infrastructure interfaces.

Examples:

AIService.generate()

EmbeddingService.embed()

PromptRegistry.load()

ModelRouter.select()

ToolExecutor.execute()

Business APIs come later.

Testing

Create tests for:

Provider adapters
Prompt validation
Model routing
Structured output
Tool execution
Context management
Memory
Retry logic
Error handling

Use the Mock Provider to avoid external API calls during testing.

Coverage target:

≥95%

Documentation

Generate:

docs/ai/

README.md

provider-architecture.md

prompt-management.md

model-routing.md

structured-output.md

tool-framework.md

context-management.md

memory-system.md

evaluation-framework.md
Quality Gates

Loop fails if:

❌ LangGraph agents exist

❌ Reservation assistant exists

❌ Concierge exists

❌ RAG exists

❌ Business workflows call LLMs

❌ FastAPI AI endpoints expose business functionality

Those belong to later loops.

Acceptance Criteria

The AI Platform should:

Support multiple providers
Route requests dynamically
Validate structured outputs
Manage prompts independently
Support tool execution
Handle context safely
Record telemetry
Cache responses
Support evaluation
Pass all tests
Definition of Done

Loop 07 is complete only if:

Provider abstraction implemented.
Prompt registry operational.
Model registry complete.
Model router functional.
Structured output validated.
Tool framework implemented.
Memory interfaces defined.
Context management operational.
AI telemetry implemented.
Evaluation framework created.
Documentation complete.
Tests passing.
Exit Criteria

At the end of Loop 07:

HospitalityAI possesses a complete AI infrastructure platform that can power any AI capability without depending on a specific provider or business module.

No business logic, agents, or RAG have been implemented yet.

The platform is now ready for Loop 08 — Multi-Agent Platform, where LangGraph orchestration, planners, supervisors, workflows, and autonomous agent execution will be built on top of this AI infrastructure.

Engineering Notes for Antigravity

Before implementation:

Read all previous loops and execution-rules.md.
Design clear interfaces before writing implementations.
Implement provider abstractions before concrete providers.
Use dependency injection for all AI services.
Ensure every component is independently testable.
Avoid provider-specific logic outside the provider adapters.
Treat prompts as versioned assets, not inline strings.
Use the Mock Provider extensively to keep tests deterministic and independent of external APIs.


Should generate

.specs/ai/

provider.md

prompt-registry.md

tool-system.md

context-manager.md

memory.md

structured-output.md

evaluation.md

before implementation.