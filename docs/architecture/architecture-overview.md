# Architecture Overview

HospitalityAI is built as a modular system organized into decoupled, logical platforms. The platform optimizes for development efficiency, testing rigor, and operational stability.

## 1. System Topology
The platform is organized as a modular monolith containing strict domain boundaries. This combines the deployment simplicity of a single container with the clean isolation patterns of microservices.

```
       ┌─────────────────────────────────────────────────────────┐
       │                       Frontend UI                       │
       └────────────────────────────┬────────────────────────────┘
                                    │ HTTP / REST
       ┌────────────────────────────▼────────────────────────────┐
       │                     FastAPI Gateway                     │
       └────────────────────────────┬────────────────────────────┘
                                    │ In-process Call / Event
       ┌────────────────────────────▼────────────────────────────┐
       │                     Business Core                       │
       │   ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ │
       │   │  Reservation  │ │     Guest     │ │  Operations   │ │
       │   └───────────────┘ └───────────────┘ └───────────────┘ │
       └────────────┬────────────────────────────────┬───────────┘
                    │                                │
       ┌────────────▼──────────────┐   ┌─────────────▼───────────┐
       │        AI Platform        │   │      Data Platform      │
       │   ┌──────────┐┌─────────┐ │   │   ┌────────┐┌────────┐  │
       │   │  Agent   ││  RAG    │ │   │   │ Postgres││ Redis  │  │
       │   │ Orchestr.││ Retrieve│ │   │   └────────┘└────────┘  │
       │   └──────────┘└─────────┘ │   └─────────────────────────┘
       └───────────────────────────┘
```

## 2. Logical Platforms

1. **API Platform (`api/`)**: Serves as the traffic gateway. It authenticates users, checks token scopes, validates Pydantic payloads, handles rate limits, and maps routes. It has no business logic.
2. **Business Platform (`business/`)**: Houses the domain rules, entities, and services. Business modules (Reservations, Operations, etc.) are isolated and can only communicate through defined API boundaries or asynchronous events.
3. **AI Platform (`ai/`)**: Standardizes LLM integrations, adapter patterns, prompt registries, structured validation, and token cost logging.
4. **Agent Platform (`agents/`)**: Implements stateful multi-agent workflows using LangGraph, utilizing supervisors, executors, planners, and human-in-the-loop triggers.
5. **Knowledge Platform (`knowledge-platform/` & `rag/`)**: Manages ingestion pipelines, document parsing, embeddings, Qdrant vector index storage, and semantic searches.
6. **ML Platform (`ml/`)**: Trains models (forecasting, sentiment, cancellations) and conducts inference, logging metrics via MLflow and storing data in MinIO.
7. **Data Platform (`database/` & `etl/`)**: Handles relational databases (PostgreSQL), migrations (Alembic), ETL tasks, and caches (Redis).

## 3. Rationale behind key decisions
- **Modular Monolith**: Eliminates the overhead of microservices (network latencies, complex routing, distributed transactions) while retaining clean separation of domain boundaries.
- **Provider Decoupling**: All platform services communicate via abstract interfaces. Swapping databases (PostgreSQL to MySQL) or LLMs (Gemini to Claude) only requires writing a new adapter implementation.
- **Async-First Execution**: Non-blocking IO ensures the system can handle concurrent operations and API responses efficiently.
