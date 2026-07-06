# Spec: Structured Logging

- **Status**: Ready
- **Owner**: DevOps Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define log structures, log levels, and processors for JSON logs output.

## 2. Log Message Schema
All log items printed to stdout must conform to structured JSON layout:
```json
{
  "timestamp": "2026-07-04T12:00:00.000Z",
  "level": "info",
  "logger": "backend.api.middleware",
  "message": "HTTP Request Completed",
  "request_id": "req-1122",
  "http_method": "POST",
  "http_path": "/api/v1/reservations",
  "status_code": 201,
  "latency_ms": 15.4
}
```

## 3. Data Sanitization and Secrets Filtering
- The logging pipeline must screen parameters keys.
- If a parameter key matches credentials names (e.g. `password`, `token`, `secret`, `api_key`), the value must be replaced with `[REDACTED]`.
