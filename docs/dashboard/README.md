# Executive Intelligence Platform (README)

## Purpose
The Executive Intelligence Platform (BFF) integrates data from the Reservations, Guest, Operations, and Revenue platforms into a unified API suite. It powers executive layouts, AI reports, threshold warnings, and conversational assistant widgets.

## Ownership
- **Owner**: Frontend & Dashboard Platform Team
- **Primary Domain**: API Orchestration, UI Widgets, Report Compilation, Assistant Agents

## Structure
```
dashboard/
├── api/             # REST endpoints (layout, executive overview, analytics, exports)
├── permissions/     # RBAC middlewares verifying user context roles
├── executive/       # Health calculations and overview aggregates
├── widgets/         # Component widget format standardizers
├── alerts/          # Alert Engine evaluating operational limits
├── forecasting/     # Visual curves consolidation
├── reports/         # AI-enhanced reporting (Daily, Weekly, Monthly)
├── ai/              # LangGraph Executive Assistant StateGraph
└── exports/         # Exporter for CSV, Excel, JSON, and PDF
```

## APIs
- `GET /dashboard/layout`: Retrieve role grid mapping configuration.
- `GET /dashboard/executive`: Retrieve aggregated KPIs and widgets.
- `GET /dashboard/revenue`: Fetch sliced revenue metrics.
- `GET /dashboard/operations`: Fetch sliced housekeeping SLAs.
- `GET /dashboard/guests`: Fetch guest loyalty distributions.
- `GET /dashboard/alerts`: Fetch active threshold warnings.
- `GET /dashboard/forecasts`: Retrieve demand and revenue curves.
- `GET /dashboard/reports`: List previous reports.
- `POST /dashboard/reports/generate`: Run AI reporting engine.
- `GET /dashboard/decisions`: Retrieve historic pricing recommendations.
- `POST /dashboard/assistant`: Query the AI agent.
- `POST /dashboard/exports`: Download PDF, Excel, CSV, or JSON datasets.
- `POST /dashboard/visual-analytics/explain`: Converts chart values to dynamic natural text explanation.
