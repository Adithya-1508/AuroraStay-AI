# ADR-0003: Vector Database Selection

- **Status**: Approved
- **Date**: 2026-07-04
- **Author**: Antigravity AI Coding Agent
- **Owner**: Knowledge Platform
- **Supersedes**: None

## Context
The AI Concierge requires the ability to answer guest queries using the hotel's static documentation (RAG). This requires storing text chunk embeddings, running fast cosine-similarity searches, and applying strict metadata filtering (e.g. limiting search to specific document categories or guest profiles) to prevent unauthorized data exposure.

## Decision
We select **Qdrant** as our primary vector database.
- It will run as a local container and be accessed via the async `qdrant-client` library.
- The platform will interact with Qdrant exclusively through adapters inside the `knowledge-platform/` and `rag/` directories.

## Rationale
- **Payload-Based Filtering**: Qdrant supports advanced metadata filtering during similarity search, allowing the system to run filters (e.g., guest scopes) on the payload without affecting search latency.
- **Developer Experience**: Offers a rich async Python SDK, a clean REST API, and a built-in Web UI dashboard for inspecting vector collections.
- **Lightweight Footprint**: Written in Rust, Qdrant is fast and consumes minimal RAM and CPU in Docker, making it ideal for unified container deployments.

## Alternatives Considered
- **pgvector**: Evaluated as a PostgreSQL extension. While pgvector is simple for single-database setups, it lacks advanced search optimizations and payload filtering controls compared to a dedicated engine like Qdrant.
- **Pinecone**: Rejected because it is a closed-source, cloud-only service. This violates our offline-first and unified local containerization targets.

## Consequences
- **Pros**:
  - Extremely fast sub-10ms search latencies.
  - Robust payload filtering for security contexts.
- **Cons/Risks**:
  - Adds another container to our deployment stack.
- **Migration/Rollout**:
  - Qdrant integration will be configured and verified in Loop 09.
