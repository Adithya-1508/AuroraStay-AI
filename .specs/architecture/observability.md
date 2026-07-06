# Spec: Observability & Telemetry

- **Status**: Ready
- **Owner**: Infrastructure & Operations Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define structured JSON logging properties, Prometheus metric collectors, and OpenTelemetry distributed tracing context propagations.

## 2. Responsibilities
- Intercept logs and format them into standard JSON structures.
- Expose system metrics via a `/metrics` scrape endpoint.
- Register and propagate correlation IDs across HTTP calls, Redis queues, and LLM requests.
- Track LLM token usage counts, categorizing costs by model name and session IDs.

## 3. Dependencies
- **OpenTelemetry SDK**: Distributed tracing framework.
- **Prometheus Client**: Metrics exporter library.
- **structlog**: Python structured logging formatter.

## 4. Public Interfaces
```python
class TelemetryTracer:
    def start_span(self, span_name: str, correlation_id: str) -> SpanContext:
        """Starts a traceable execution span."""
        pass

class MetricsCollector:
    def increment_counter(self, metric_name: str, labels: Dict[str, str]) -> None:
        """Increments a counter metric (e.g. API requests count)."""
        pass
```

## 5. Configuration
- `OTEL_EXPORTER_OTLP_ENDPOINT`: Target OTLP trace collector endpoint.
- `PROMETHEUS_METRICS_PORT`: Scrape port (default: `8000/metrics`).
- `LOG_LEVEL`: Output logging filter (default: `INFO`).

## 6. Failure Modes
- **OTLP Exporter Down**: If the trace exporter fails, drop trace spans in memory to prevent memory leaks, logging a warning. The application must not crash.
- **Metrics Scraping Failure**: Ensure scrape errors do not interfere with active HTTP request execution paths.

## 7. Security Considerations
- Never log user-sensitive attributes (names, credit cards, emails) in trace tags or JSON log payloads.
- Sanitize stack traces to prevent internal server details from leaking to users.

## 8. Testing Strategy
- **Unit Tests**: Verify log formats contain mandatory keys (correlation ID, timestamp, level).
- **Integration Tests**: Verify that trace headers propagate correctly across in-process service calls.
