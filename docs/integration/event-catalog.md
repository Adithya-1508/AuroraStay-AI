# Event Catalog & Signals Mappings

This document catalogs internal event-driven signals and metrics events within HospitalityAI.

## In-App Events Catalog

### 1. `RESERVATION_CREATED`
- **Trigger**: Fired when guest reservation is successfully completed.
- **Subscribers**:
  - `AllocationEngine`: Allocates guest rooms.
  - `HistoryService`: Appends history log entry.
  - `AuditTrail`: Appends cryptographic SHA-256 block hash.
- **Payload Data**: `reservation_id`, `guest_id`, `allocated_room`.

### 2. `SECURITY_INCIDENT_FLAGGED`
- **Trigger**: Fired when AI guardrails detect prompt injection or rate-limit violations.
- **Subscribers**:
  - `IncidentTracker`: Creates incident containment tickets.
  - `AuditTrail`: Appends audit record.
  - `AlertConsole`: Displays red metrics warnings in Streamlit dashboard.
- **Payload Data**: `incident_id`, `title`, `severity`, `source_ip`.
