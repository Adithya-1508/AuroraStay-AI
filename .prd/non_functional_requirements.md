# Non-Functional Requirements

This document establishes the technical, quality, security, and performance constraints for HospitalityAI.

---

## 1. Performance and Latency Targets

- **NFR-101: API Response Time**: Internal REST API endpoints (e.g. reservation search, housekeeping updates) must return responses within $\le 200\text{ ms}$ under normal load conditions.
- **NFR-102: Conversational AI Latency**: AI Concierge response generation (retrieval + LLM generation) must complete within $\le 2.0\text{ seconds}$ to maintain natural conversation pacing.
- **NFR-103: Dashboard Load Time**: The analytics dashboard index page must render fully within $\le 1.5\text{ seconds}$.
- **NFR-104: Database Query Speed**: SQL database queries must use proper indexing to keep execution times under $\le 50\text{ ms}$.

---

## 2. Reliability and High Availability

- **NFR-201: Graceful Degradation**: If the external LLM provider is down or times out, the AI Concierge must automatically fall back to a predefined message apologizing for the delay and offering front desk phone numbers.
- **NFR-202: Health Check Endpoints**: Every platform service must expose a `/health` endpoint returning database connection health, cache connectivity status, and background worker state.
- **NFR-203: Transaction Integrity**: Reservation bookings and room status changes must operate under ACID transactions. The system must prevent overbookings in race conditions.

---

## 3. Security & Compliance

- **NFR-301: Authentication**: All private routes must require JSON Web Tokens (JWT) using the RS256 signing algorithm.
- **NFR-302: Authorization (RBAC)**: Access levels must follow the Principle of Least Privilege:
  - `Guest`: Can read/write their own reservations and use the AI Concierge.
  - `Staff`: Can manage all reservations, view logs, update room statuses.
  - `Manager`: Access to pricing configurations, revenue analytics, and forecasts.
  - `Admin`: Full access to database, secrets, and audit logs.
- **NFR-303: Data Encryption**: Sensitive guest information (names, emails, phone numbers) must be encrypted at rest and in transit (using HTTPS/TLS 1.3).

---

## 4. Maintainability and Extensibility

- **NFR-401: Test Coverage**: The project code must maintain an automated test coverage of $\ge 90\%$.
- **NFR-402: Decoupled Platforms**: Platforms (API, AI, ML, Data, Knowledge) must only communicate through public contracts, ensuring individual components can be rewritten without systemic impact.
- **NFR-403: Provider Adapters**: Swapping a vendor database or LLM model must require zero business logic changes.

---

## 5. Observability and Telemetry

- **NFR-501: Structured Logging**: All application logs must be output in JSON format, capturing `timestamp`, `log_level`, `module`, `session_id`, `user_id`, and `message`.
- **NFR-502: Telemetry Tracing**: LLM API calls and agent pipelines must be instrumented with tracing tags (e.g. token counts, model names, temperature, latency) to audit operational costs.
