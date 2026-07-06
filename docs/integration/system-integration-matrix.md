# System Integration Matrix

This matrix documents the communication interfaces, ports, protocols, and data schemas shared between the logical subsystems of HospitalityAI.

## Subsystem Communications Matrix

| Source Subsystem | Destination Subsystem | Protocol | Port / Endpoint | Payload / Data Schema | Purpose |
| --- | --- | --- | --- | --- | --- |
| **Frontend Web UI** | **API Gateway** | REST / HTTP | `8000/api/v1/*` | JSON (Reservation, Guest schemas) | Fetching dashboard data, booking room requests, checking in guests. |
| **Frontend Web UI** | **API Gateway (Chat)** | WebSocket | `8000/api/v1/chat/ws` | JSON Chat messages (session, text, sender) | Interactive conversational chat with the AI Concierge. |
| **API Gateway** | **PostgreSQL** | SQL / Asyncpg | `5432` | Binary / Parameterized queries | CRUD operations on reservation, guest, room, and task tables. |
| **API Gateway** | **Redis (Cache)** | Redis Protocol | `6379` | Key-Value / JSON chat history | Retrieving transient session states and caching nightly room rates. |
| **API Gateway** | **Redis (Events)** | Redis PubSub | `6379` | JSON Event (event_type, timestamp, data) | Publishing events (e.g. `reservation.checkout`) for background tasks. |
| **API Gateway** | **Qdrant** | gRPC / REST | `6333` | Point Struct vectors + payloads | Cosine-similarity searches for matching FAQ embedding contexts. |
| **API Gateway** | **MLflow** | REST / HTTP | `5000` | REST API requests | Loading the active forecasting model configurations. |
| **API Gateway** | **MinIO** | S3 API | `9000` | S3 Object requests | Loading document inputs or fetching model binary weights files. |
| **API Gateway** | **LLM API** | HTTPS REST | `443` | JSON Prompt + schema parameters | Invoking the model provider to obtain chat answers. |
| **Queue Worker** | **Redis (Events)** | Redis Protocol | `6379` | Redis Queue pop | Listening to background task messages. |
| **ML Pipeline** | **MLflow** | REST / HTTP | `5000` | REST API log requests | Logging forecasting loss scores and registering model tags. |
| **API / Worker** | **OTLP Collector** | OTLP / gRPC | `4317` | OpenTelemetry span payloads | Exporting distributed traces, spans, and Prometheus indicators. |
