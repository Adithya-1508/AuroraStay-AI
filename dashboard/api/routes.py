from typing import Any, cast

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel

from backend.auth.permissions import get_current_user_context
from dashboard.ai.assistant import ExecutiveAssistantAgent
from dashboard.analytics.service import AnalyticsService
from dashboard.executive.service import ExecutiveService
from dashboard.exports.engine import ExportEngine
from dashboard.forecasting.service import DashboardForecastingService
from dashboard.layouts.service import LayoutService
from dashboard.permissions.guard import (
    require_executive,
    require_guest,
    require_operations,
    require_revenue,
)
from dashboard.reports.engine import AIReportingEngine

router = APIRouter(prefix="/dashboard")


# Request Schemas
class GenerateReportRequest(BaseModel):
    interval: str
    department: str
    custom_notes: str | None = None


class AssistantQueryRequest(BaseModel):
    query: str


class ExportRequest(BaseModel):
    export_format: str
    dataset_type: str
    filters: dict[str, Any] = {}


class VisualAnalyticsRequest(BaseModel):
    chart_type: str
    metric_name: str
    historical_data: list[float]
    forecast_data: list[float]


# Routes
@router.get("/layout", tags=["Dashboard"])
async def get_dashboard_layout(
    user: dict[str, Any] = Depends(get_current_user_context),
) -> dict[str, Any]:
    """Retrieves the layout configuration based on the authenticated user's role."""
    role = user.get("role", "Staff")
    return LayoutService.get_layout_for_role(role)


@router.get("/executive", tags=["Dashboard"])
async def get_executive_overview(
    user: dict[str, Any] = Depends(require_executive),
) -> dict[str, Any]:
    """Retrieves the aggregated executive overview KPIs, widgets, and alerts."""
    service = ExecutiveService()
    # Mocking aggregated indicators from the other platform services
    return service.get_overview(
        occupancy_rate=0.74,
        last_month_occupancy=0.72,
        today_arrivals=12,
        today_departures=8,
        total_billing=12450.00,
        adr=150.00,
        revpar=111.00,
        trend_percentage=4.5,
        sparkline=[110, 115, 120, 118, 125, 122, 124],
        forecast_occupancy=[0.75, 0.76, 0.78, 0.79, 0.81, 0.80, 0.82],
        forecast_labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        clean_rooms=45,
        dirty_rooms=10,
        in_progress_rooms=5,
        sla_compliance=0.92,
        pending_tasks=15,
        avg_guest_satisfaction=4.6,
        cancellations_today=3,
    )


@router.get("/revenue", tags=["Dashboard"])
async def get_revenue_dashboard(
    user: dict[str, Any] = Depends(require_revenue),
) -> dict[str, Any]:
    """Retrieves high-level sliced analytics for revenue categories."""
    return AnalyticsService.get_sliced_analytics(
        department="Revenue",
        revenue_source="room",
    )


@router.get("/operations", tags=["Dashboard"])
async def get_operations_dashboard(
    user: dict[str, Any] = Depends(require_operations),
) -> dict[str, Any]:
    """Retrieves operational KPIs and housekeeper tasks turnaround metrics."""
    return AnalyticsService.get_sliced_analytics(
        department="housekeeping",
    )


@router.get("/guests", tags=["Dashboard"])
async def get_guests_dashboard(
    user: dict[str, Any] = Depends(require_guest),
) -> dict[str, Any]:
    """Retrieves guest satisfaction and loyalty demographic distributions."""
    return AnalyticsService.get_sliced_analytics(
        guest_segment="leisure",
    )


@router.get("/alerts", tags=["Dashboard"])
async def get_active_alerts(
    user: dict[str, Any] = Depends(require_operations),
) -> list[dict[str, Any]]:
    """Retrieves critical alert warnings evaluated across platforms."""
    service = ExecutiveService()
    overview = service.get_overview(
        occupancy_rate=0.35,  # triggers low occupancy alert
        last_month_occupancy=0.72,
        today_arrivals=12,
        today_departures=8,
        total_billing=12450.00,
        adr=150.00,
        revpar=111.00,
        trend_percentage=4.5,
        sparkline=[110, 115, 120, 118, 125, 122, 124],
        forecast_occupancy=[0.35] * 7,
        forecast_labels=["Mon"] * 7,
        clean_rooms=45,
        dirty_rooms=2,
        in_progress_rooms=5,
        sla_compliance=0.85,  # triggers SLA warning
        pending_tasks=15,
        avg_guest_satisfaction=3.2,  # triggers sentiment alert
        cancellations_today=6,  # triggers cancellation warning
        model_drift=0.30,  # triggers drift warning
        rag_confidence=0.20,  # triggers RAG warning
    )
    return cast(list[dict[str, Any]], overview["alerts"])


@router.get("/forecasts", tags=["Dashboard"])
async def get_occupancy_forecasts(
    horizon_days: int = 30,
    room_type_id: str | None = None,
    compare_historical: bool = True,
    user: dict[str, Any] = Depends(require_revenue),
) -> dict[str, Any]:
    """Retrieves occupancy, demand, and expected revenue trend curves."""
    return DashboardForecastingService.get_forecast_payload(
        horizon_days=horizon_days,
        room_type_id=room_type_id,
        compare_historical=compare_historical,
    )


@router.get("/reports", tags=["Dashboard"])
async def list_previous_reports(
    user: dict[str, Any] = Depends(require_executive),
) -> list[dict[str, Any]]:
    """Lists generated report metadata archives."""
    return [
        {
            "id": "rep-prev-1",
            "title": "Weekly Performance Summary",
            "interval": "WEEKLY",
            "department": "ALL",
            "generated_at": "2026-07-01T12:00:00Z",
        }
    ]


@router.post("/reports/generate", tags=["Dashboard"])
async def generate_ai_report(
    req: GenerateReportRequest,
    user: dict[str, Any] = Depends(require_executive),
) -> dict[str, Any]:
    """Triggers the AI Report Engine to compile a structured summary."""
    engine = AIReportingEngine()
    report = await engine.generate_report(
        interval=req.interval,
        department=req.department,
        custom_notes=req.custom_notes,
    )
    return report.model_dump()


@router.get("/decisions", tags=["Dashboard"])
async def get_decision_intelligence_records(
    user: dict[str, Any] = Depends(require_revenue),
) -> list[dict[str, Any]]:
    """Retrieves historic pricing optimization and dynamic markup recommendations."""
    return [
        {
            "id": "dec-101",
            "timestamp": "2026-07-08T09:30:00Z",
            "action": "Deluxe room markup adjusted from +15% to +20%",
            "reason": "Predicted occupancy threshold exceeded (88%)",
            "expected_impact": "+$1,400 revenue weekly",
            "confidence_score": 0.94,
        }
    ]


@router.post("/assistant", tags=["Dashboard"])
async def query_executive_assistant(
    req: AssistantQueryRequest,
    user: dict[str, Any] = Depends(require_executive),
) -> dict[str, Any]:
    """Queries the LangGraph assistant agent for business answers and anomaly explanations."""
    agent = ExecutiveAssistantAgent()
    return await agent.ask_question(req.query)


@router.post("/exports", tags=["Dashboard"])
async def export_dashboard_dataset(
    req: ExportRequest,
    user: dict[str, Any] = Depends(require_executive),
) -> Response:
    """Generates downloable datasets in CSV, Excel, JSON, or PDF formats."""
    try:
        data_bytes = ExportEngine.export_dataset(
            export_format=req.export_format,
            dataset_type=req.dataset_type,
            filters=req.filters,
        )

        content_types = {
            "JSON": "application/json",
            "CSV": "text/csv",
            "EXCEL": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "PDF": "application/pdf",
        }
        mime = content_types.get(req.export_format.upper(), "application/octet-stream")
        ext = req.export_format.lower()
        if ext == "excel":
            ext = "xls"

        headers = {
            "Content-Disposition": f"attachment; filename=export_{req.dataset_type.lower()}_20260708.{ext}"
        }
        return Response(content=data_bytes, media_type=mime, headers=headers)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate export file: {e}",
        ) from e


@router.post("/visual-analytics/explain", tags=["Dashboard"])
async def explain_chart_visuals(
    req: VisualAnalyticsRequest,
    user: dict[str, Any] = Depends(require_executive),
) -> dict[str, Any]:
    """Converts raw chart trends into plain explanation summaries with causes and impact."""
    hist_avg = sum(req.historical_data) / max(len(req.historical_data), 1)
    fore_avg = sum(req.forecast_data) / max(len(req.forecast_data), 1)

    diff = fore_avg - hist_avg
    direction = "increased" if diff > 0 else "decreased"
    pct = (abs(diff) / hist_avg * 100) if hist_avg > 0 else 0

    return {
        "status": f"{req.metric_name} is projected to be {direction} by {pct:.1f}% compared to historical levels.",
        "causes": [
            f"Increased weekend bookings pushing {req.metric_name} upwards"
            if diff > 0
            else f"Seasonality downturn weighing on {req.metric_name}"
        ],
        "actions": [
            "Introduce premium upsells to capture higher booking volume"
            if diff > 0
            else "Deploy marketing discounts to offset the forecasted decline"
        ],
        "expected_impact": abs(diff) * 1.5,
    }
