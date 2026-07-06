# Container Diagram (C4 Level 2)

This container diagram details the architectural components (containers) within the HospitalityAI platform boundaries, demonstrating the database, storage, and caching subsystems.

## 1. Container Diagram

```mermaid
graph TB
    %% Users
    Guest["Guest"]
    Staff["Hotel Staff"]

    subgraph Platform Bounds ["HospitalityAI Platform Container Boundary"]
        %% Frontend
        FE["Frontend Web UI<br>(Vanilla HTML/JS/CSS Dashboard)"]

        %% Gateway
        GW["FastAPI API Gateway<br>(Python API Web Server)"]

        %% Background Worker
        Worker["Background Queue Worker<br>(In-process Async Tasks)"]

        %% Caches and DBs
        DB[("PostgreSQL Database<br>(Transactional Store)")]
        Cache[("Redis cache & PubSub<br>(Session / Event Store)")]
        VecDB[("Qdrant Vector DB<br>(FAQ Embeddings Store)")]
        MinIO[("MinIO Object Storage<br>(Documents / ML Models)")]
        MLflow[("MLflow Tracking Server<br>(Model Registry)")]
    end

    %% External
    LLM["External LLM Provider<br>(Gemini, Claude)"]

    %% Connections
    Guest -->|"HTTP / Web Chat"| FE
    Staff -->|"HTTP / Web Dashboard"| FE

    FE -->|"REST / JSON APIs (Port 8000)"| GW
    GW -->|"Read/Write (Port 5432)"| DB
    GW -->|"Cache / Publish (Port 6379)"| Cache
    GW -->|"Query embeddings (Port 6333)"| VecDB
    GW -->|"Read/Write models (Port 9000)"| MinIO
    GW -->|"Query models (Port 5000)"| MLflow
    GW -->|"Invokes adapters (HTTPS)"| LLM

    Worker -->|"Listen to Queue"| Cache
    Worker -->|"Query/Mutate"| DB
    Worker -->|"Update vector index"| VecDB
    Worker -->|"Load models / files"| MinIO
```

## 2. Container Descriptions and Communications

- **Frontend Web UI**: Client-side application rendering the analytics dashboard and guest chat widget. Communicates with the API gateway via HTTPS REST requests.
- **FastAPI API Gateway**: Runs the core web service. Handles authentication, delegates bookings to application modules, forwards vector requests, and issues async tasks.
- **Background Queue Worker**: Processes asynchronous background events (e.g. training prediction models, document chunk processing, housekeeping task generation) via Redis-backed task loops.
- **PostgreSQL Database**: The relational transactional persistence engine. Holds guest profiles, reservation calendar records, room details, and housekeeping logs.
- **Redis Cache & Pub/Sub**: Manages transient session states, active user keys, chat window histories, and inter-service messaging queues.
- **Qdrant Vector DB**: Powers retrieval-augmented generation (RAG) by storing high-dimensional semantic FAQ document embeddings.
- **MinIO Object Storage**: S3-compatible local bucket storing static documents, raw reviews for pipelines, and pickled machine learning models.
- **MLflow Tracking Server**: Tracks model runs, loss histories, and manages forecasting deployment model registries.
- **External LLM Provider**: Process chat contexts via API adapters.
