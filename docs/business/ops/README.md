# Hotel Operations Platform (HOP)

The **Hotel Operations Platform (HOP)** manages physical hotel logistics: room turnaround housekeeping activities, resource assignments, and maintenance repair work orders.

## Architecture & Workflows

```mermaid
graph TD
    A[Checkout Event] -->|Auto Dispatch| B(OperationsService)
    B -->|Create| C[HousekeepingTask]
    D[Staff Request] -->|Manual Create| B
    B -->|Assign Employee| E[Task In Progress]
    E -->|Complete Turnaround| F[Room Status: Clean]
    
    G[Maintenance Request] -->|Priority: Urgent| H[Room Status: Under Maintenance]
    G -->|Priority: Low/Medium| I[Room Status: Active]
    J[Technician Completes Repair] -->|Transition| F
```

## Platform Elements

1. [Housekeeping Tracking](housekeeping.md)
   Details turnaround logistics, checkout hooks, status tracking, and employee assignments.
2. [Maintenance Management](maintenance.md)
   Documents work order priorities (`LOW`, `MEDIUM`, `URGENT`), and target room state transitions.
3. [API Specifications](api.md)
   Exposes complete REST endpoints reference grid for operations integrations.
