# Observability Architecture

HospitalityAI implements extensive telemetry using OpenTelemetry standards, Prometheus endpoints, and structured JSON logs.

## 1. Trace Propagation Flow

```
   HTTP request (Correlation-ID: 'corr_abc')
     │
     ▼
   FastAPI Gateway (Span 1: Endpoint Request)
     │
     ├─► Business logic (Span 2: UseCase execution)
     │     │
     │     ├─► PostgreSQL (Span 3: DB Query)
     │     │
     │     └─► AI Platform (Span 4: LLM Adapter Request)
     │
     ▼
   HTTP Response (Correlation-ID: 'corr_abc')
```

- Every API request generates a unique `Correlation-ID` header.
- This ID propagates to Redis events, celery workers, and LLM telemetry traces, providing cross-system auditing.

---

## 2. Telemetry Configurations

### A. JSON Logs Format
Logs are written to standard output (`stdout`) in JSON formatting:
```json
{
  "timestamp": "2026-07-04T17:00:00.123Z",
  "log_level": "INFO",
  "correlation_id": "corr_abc",
  "user_id": "gst_9988",
  "module": "api.routes.reservations",
  "message": "Reservation created successfully",
  "metadata": {
    "reservation_id": "res_12345",
    "room_type": "Deluxe"
  }
}
```

### B. Prometheus Metrics
The system exposes standard metrics at `GET /metrics`:
- **`http_request_duration_seconds`**: Histogram tracking REST route execution latency.
- **`ai_token_usage_total`**: Counter tracking token consumption grouped by `model_name` and `direction` (input vs output).
- **`ai_request_latency_seconds`**: Histogram tracking conversational retrieval + LLM durations.
- **`housekeeping_task_completion_minutes`**: Gauge tracking housekeeping task turnaround speeds.
- **`db_connection_pool_active`**: Gauge tracking active SQLAlchemy connection pools.
