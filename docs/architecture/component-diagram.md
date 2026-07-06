# Component Diagram (C4 Level 3)

This component diagram zooms into the internal components of the **Reservations** and **AI Concierge** services inside the API Gateway and Business Core containers.

## 1. Component Diagram

```mermaid
graph TB
    subgraph FastAPI API Gateway
        subgraph Reservation Component Group
            RC["Reservation Controller<br>(API routes & schemas)"]
            RS["Reservation Service<br>(Application logic)"]
            Price["Pricing Engine<br>(Seasonal calculators)"]
            Avail["Availability Engine<br>(Overlap checks)"]
            RR["Reservation Repository Interface"]
            RImpl["PostgreSQL Reservation Repository<br>(Infrastructure DB calls)"]
        end

        subgraph AI Concierge Component Group
            CC["Chat Controller<br>(Web socket / REST chat)"]
            CS["Chat Service<br>(Orchestrator)"]
            RAG["RAG Retrieval Service<br>(Context builder)"]
            Prompt["Prompt Registry<br>(Prompt templates)"]
            LLMA["LLM Adapter Gateway<br>(API callers)"]
            Hand["Handoff Supervisor<br>(Escalation controller)"]
        end
    end

    DB[("PostgreSQL DB")]
    VecDB[("Qdrant Vector DB")]
    LLM["LLM API"]

    %% Reservation flows
    RC -->|"Calls"| RS
    RS -->|"Checks pricing"| Price
    RS -->|"Checks overlap"| Avail
    RS -->|"Queries/Mutates"| RR
    RR -->|"Implemented by"| RImpl
    RImpl -->|"SQL Queries"| DB

    %% Chat flows
    CC -->|"Delegates"| CS
    CS -->|"Retrieves context"| RAG
    CS -->|"Gets template"| Prompt
    CS -->|"Calls adapter"| LLMA
    CS -->|"Monitors sentiment/rules"| Hand
    RAG -->|"Embeddings search"| VecDB
    LLMA -->|"HTTPS Prompt"| LLM
```

## 2. Component Descriptions

### Reservations Group
- **Reservation Controller**: Declares REST endpoints (e.g. `POST /api/v1/reservations/`). Validates payloads using Pydantic models and parses date objects.
- **Reservation Service**: Coordinates core reservation use cases. Dictates transactional database scopes, checks room capacities, and raises domain errors.
- **Pricing Engine**: Extends reservations business logic by calculating total booking rates, factoring in base costs, days of the week, and holiday multipliers.
- **Availability Engine**: Checks inventory capacity for the check-in and check-out dates, preventing overbooking.
- **Reservation Repository**: Encapsulates DB details. Declares abstract SQL interfaces to maintain database independence.
- **PostgreSQL Reservation Repository**: Implements SQL database access utilizing SQLAlchemy async methods.

### AI Concierge Group
- **Chat Controller**: Handles WebSocket or polling REST requests for the chat widget.
- **Chat Service**: Manages stateful conversational logic, merging user input, history, and retrieved context.
- **RAG Retrieval Service**: Interacts with the Vector database to search, retrieve, and format the context blocks needed for prompt completion.
- **Prompt Registry**: System asset repository containing modular, version-controlled prompt files (YAML or text format).
- **LLM Adapter Gateway**: Translates structured system prompts into provider-specific API calls, handling error retry flows.
- **Handoff Supervisor**: Intercepts chat pipelines to check for angry sentiment, agent loops, or explicit human requests, triggering receptionist queues.
