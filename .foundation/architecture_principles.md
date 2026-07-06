# Architecture Principles

The architecture of HospitalityAI is designed to scale, resist regression, and maintain clean separation of concerns.

## 1. Layered Architecture
We strictly enforce a 4-tier layered architecture:

1. **Presentation Layer**: Responsible for REST controllers, routes, API serialization, and input validation. No business rules are allowed here.
2. **Application Layer**: Orchestrates use cases, manages transactions, and delegates actions to domain services.
3. **Domain Layer**: Houses core business logic, aggregates, entities, value objects, and business invariants. This layer has zero dependencies on frameworks, databases, or libraries.
4. **Infrastructure Layer**: Implements gateways, database repositories, email providers, and message queue connections.

## 2. Dependency Direction Rule
Dependencies must flow inwards:

```
Presentation ──> Application ──> Domain <── Infrastructure
```

- High-level policy must never depend on low-level detail.
- Interfaces (e.g. repository interfaces) are declared in the Domain/Application layer. Their implementations are defined in the Infrastructure layer (Dependency Injection).

## 3. Bounded Context & Persistence Isolation
- Each service/platform must own its own domain boundary.
- **No service may access another service's database directly**. Inter-service data sharing must occur via APIs or events.
- Logic is encapsulated; internal data models are hidden behind public DTOs.

## 4. Communication Architecture
- **REST**: Used for synchronous, low-latency API calls.
- **Asynchronous Events**: Used for non-blocking workflows.
- **Chaining Constraint**: No synchronous request chain may exceed 3 hops (Client -> Service A -> Service B -> Service C). If more steps are needed, use async workers or events.

## 5. Provider Independence
- Every infrastructure integration (LLM, Vector DB, Cache, SQL DB, Cloud) must be accessed through adapters/interfaces.
- Swapping a provider (e.g., Qdrant to Pinecone, or OpenAI to Anthropic) must require zero changes to the Domain or Application layers.
