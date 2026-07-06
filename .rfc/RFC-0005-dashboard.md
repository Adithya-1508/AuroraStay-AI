# RFC-0005: Frontend Analytics Dashboard Design

- **Author**: Antigravity AI Coding Agent
- **Status**: Draft
- **Date**: 2026-07-04
- **Target Release/Loop**: Loop 15 — Loop 16

## 1. Summary
This RFC proposes the layout structure, charting libraries, and API communications for the hotel staff dashboard.

## 2. Proposed Design

### Dashboard Layout Sections
- **Overview Pane**: Real-time KPIs (occupancy, ADR, RevPAR, guest sentiment).
- **Reservation Pane**: Searchable listing of guest stays, calendar timeline, check-in controls, and booking details.
- **Housekeeping Pane**: Grid of housekeeper tasks (dirty/clean room statuses, turnaround speeds).
- **Concierge Queue**: Live monitoring of guest chats, containing alert toggles for receptionist handoffs.
- **ML Forecast Panel**: Pacing lines charting next 30 days demand.

### Technical Stack
- **Structure**: Vanilla HTML5, CSS3, and JavaScript/TypeScript.
- **Charts**: Chart.js or D3.js for rendering occupancy pacing lines and revenue gauges.
- **Communication**: REST APIs (port 8000) for CRUD tasks. WebSockets for real-time concierge chat and housekeeping updates.

## 3. Testing and Verification
- Perform cross-browser testing and verify dashboard load times meet targets ($\le 1.5\text{ seconds}$).
