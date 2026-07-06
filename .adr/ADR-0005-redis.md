# ADR-0005: Cache and Event Broker Selection

- **Status**: Approved
- **Date**: 2026-07-04
- **Author**: Antigravity AI Coding Agent
- **Owner**: Data Platform
- **Supersedes**: None

## Context
HospitalityAI needs:
1. Fast caching of room rates and API responses.
2. Stateful chat history checkpoints to resume agent conversations.
3. Decoupled messaging channels (Pub/Sub) to trigger tasks (like creating housekeeping tasks when check-outs occur).
We need an infrastructure container that handles these requirements with sub-millisecond latencies.

## Decision
We select **Redis** as the unified platform for:
- **Caching**: Storing transient room availability data.
- **Pub/Sub Broker**: Decoupling domain event channels (`hotel_events`).
- **Session Checkpointer**: Serving as the memory persistence store for LangGraph agent sessions.

## Rationale
- **Unified Engine**: Using Redis for caching, pub/sub messaging, and session checkpoints reduces our container footprint.
- **Speed**: In-memory execution provides sub-millisecond data reads and writes.
- **Ecosystem Fit**: Redis integrates natively with Python's async Redis drivers and is the industry-standard choice for Celery/Dramatiq workers and LangGraph memory checkpointers.

## Alternatives Considered
- **RabbitMQ / Apache Kafka**: Rejected. While they are highly resilient message brokers, they add operational complexity and lack the caching and session-key storage capabilities of Redis.
- **Database Polling**: Querying PostgreSQL tables periodically to check for check-outs was rejected as it increases database load and is not real-time.

## Consequences
- **Pros**:
  - Sub-millisecond messaging and caching.
  - Multi-purpose usage reduces deployment overhead.
- **Cons/Risks**:
  - In-memory data is volatile; Redis must be configured with persistence options (AOF/RDB) to prevent data loss on crashes.
- **Migration/Rollout**:
  - Redis compose settings and async pools will be established in Loop 06.
