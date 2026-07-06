# Bounded Context Definitions

This document details the boundaries, interfaces, events, aggregates, and business rules for the 8 Bounded Contexts of HospitalityAI.

---

## 1. Reservation Context
- **Purpose**: Manages room inventory, bookings, stays, rates allocation, and calendar availability.
- **Responsibilities**:
  - Prevent overbookings.
  - Calculate stay prices.
  - Track reservation status lifecycles.
- **Public Interfaces**:
  - `ReservationService` (`search_availability`, `create_reservation`, `cancel_reservation`)
- **Inbound Events**:
  - `housekeeping.status_updated` (updates room availability cache)
- **Outbound Events**:
  - `reservation.created`
  - `reservation.cancelled`
  - `reservation.checkout`
- **Aggregates**: `Reservation` (Root)
- **Entities & Value Objects**: `Room` (Entity), `RoomCategory` (Entity), `DateRange` (Value Object), `Money` (Value Object).
- **Business Rules**: Overbooking prevention, minimum-stay bounds check.

---

## 2. Guest Context
- **Purpose**: Manages guest identities, profiles, preferences, and loyalty history.
- **Responsibilities**:
  - Create guest records.
  - Maintain CRM preferences (e.g. room temperature).
- **Public Interfaces**:
  - `GuestService` (`register_guest`, `update_preferences`)
- **Inbound Events**: None.
- **Outbound Events**:
  - `guest.registered`
- **Aggregates**: `Guest` (Root)
- **Entities & Value Objects**: `GuestProfile` (Entity), `GuestPreference` (Value Object), `LoyaltyTier` (Value Object).
- **Business Rules**: VIP categorization (loyalty tiers).

---

## 3. Operations Context
- **Purpose**: Oversees day-to-day hotel activities: housekeeping tasks and maintenance work orders.
- **Responsibilities**:
  - Automate housekeeping allocations.
  - Log task completion times.
- **Public Interfaces**:
  - `OperationsService` (`assign_task`, `complete_task`)
- **Inbound Events**:
  - `reservation.checkout` (triggers auto-housekeeping task creation)
- **Outbound Events**:
  - `housekeeping.status_updated`
  - `maintenance.completed`
- **Aggregates**: `HousekeepingTask` (Root), `MaintenanceRequest` (Root)
- **Entities & Value Objects**: `Employee` (Entity), `TaskStatus` (Value Object).
- **Business Rules**: Task sequencing (dirty rooms prioritizations based on arriving guests).

---

## 4. Revenue Context
- **Purpose**: Manages pricing rate plans and dynamically forecasts booking demand.
- **Responsibilities**:
  - Generate occupancy forecasts.
  - Calculate cancellation risks.
- **Public Interfaces**:
  - `RevenueService` (`generate_forecast`, `assess_cancellation_risk`)
- **Inbound Events**:
  - `reservation.created`, `reservation.cancelled`
- **Outbound Events**:
  - `revenue_forecast.generated`
- **Aggregates**: `RevenueForecast` (Root)
- **Entities & Value Objects**: `ForecastTimeline` (Value Object), `Occupancy` (Value Object).
- **Business Rules**: Pricing adjustments rules based on pacing levels.

---

## 5. Decision Intelligence Context
- **Purpose**: Tracks AI/ML recommendations and coordinates staff approval workflows.
- **Responsibilities**:
  - Process system recommendations.
  - Log staff decisions.
- **Public Interfaces**:
  - `DecisionService` (`review_recommendation`, `execute_decision`)
- **Inbound Events**:
  - `recommendation.generated`
- **Outbound Events**:
  - `decision.executed`
- **Aggregates**: `Recommendation` (Root), `Decision` (Root)
- **Entities & Value Objects**: `ConfidenceScore` (Value Object).
- **Business Rules**: VIP room upgrade recommendations policies.

---

## 6. Knowledge Context
- **Purpose**: Stores static FAQ documentation and routes conversational RAG inputs.
- **Responsibilities**:
  - Parse policy guides.
  - Retrieve relevant contexts.
- **Public Interfaces**:
  - `KnowledgeService` (`ingest_document`, `retrieve_faq_context`)
- **Inbound Events**: None.
- **Outbound Events**: None.
- **Aggregates**: `Conversation` (Root), `KnowledgeDocument` (Root)
- **Entities & Value Objects**: `Message` (Entity), `LanguagePreference` (Value Object).
- **Business Rules**: Context retrieval boundaries.

---

## 7. Security Context
- **Purpose**: Enforces access tokens verification and role authorization constraints.
- **Responsibilities**:
  - Issue JWT tokens.
  - Check user scopes.
- **Public Interfaces**:
  - `SecurityService` (`verify_access`, `audit_log_event`)
- **Inbound Events**: None.
- **Outbound Events**: None.
- **Aggregates**: None (Cross-cutting concern, acts as domain policies).
- **Business Rules**: RBAC authorization grids.

---

## 8. Executive Intelligence Context
- **Purpose**: Consolidates KPIs and logs audit reviews.
- **Responsibilities**:
  - Compile RevPAR, ADR reports.
- **Public Interfaces**:
  - `ExecutiveService` (`get_kpi_summary`)
- **Inbound Events**:
  - `revenue_forecast.generated`, `decision.executed`
- **Outbound Events**:
  - `executive_alert.raised`
- **Aggregates**: None (Consolidates read-models from other contexts).
- **Business Rules**: Alert thresholds definitions (e.g. occupancy dropping below target).
