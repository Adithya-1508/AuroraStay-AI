# Service Contracts & API Specifications

This document outlines key endpoint specifications and schema payload models.

## 1. Reservation Schema (`POST /api/v1/reservations`)

- **Request Payload**:
  ```json
  {
    "guest_id": "usr-123",
    "check_in": "2026-08-01",
    "check_out": "2026-08-05",
    "room_category": "Deluxe",
    "preferences": {
      "silent_room": true,
      "high_floor": false
    }
  }
  ```
- **Response Payload**:
  ```json
  {
    "reservation_id": "res-987abc",
    "status": "CONFIRMED",
    "allocated_room": "304",
    "total_cost": 650.00
  }
  ```

## 2. Telemetry Schema (`GET /api/v1/observability/telemetry`)

- **Response Payload**:
  ```json
  {
    "latency_p95_ms": 120.5,
    "active_connections": 14,
    "error_rate_percent": 0.02
  }
  ```
