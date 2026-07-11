from unittest.mock import AsyncMock, MagicMock

import pytest
from knowledge_platform.retrieval.engine import Retriever

from backend.ai.service import AIService
from dashboard.ai.assistant import ExecutiveAssistantAgent
from dashboard.alerts.engine import AlertEngine
from dashboard.analytics.service import AnalyticsService
from dashboard.executive.service import ExecutiveService
from dashboard.exports.engine import ExportEngine
from dashboard.forecasting.service import DashboardForecastingService
from dashboard.layouts.service import LayoutService
from dashboard.reports.engine import AIReportingEngine, AIReportPackage
from dashboard.widgets.service import WidgetService, WidgetStatus, WidgetType


def test_widget_builders() -> None:
    # 1. Occupancy widget
    w_occ = WidgetService.build_occupancy_widget(0.74, 0.72)
    assert w_occ.id == "widget-occupancy"
    assert w_occ.widget_type == WidgetType.VALUE
    assert w_occ.value == "74.0%"
    assert w_occ.trend is not None
    assert w_occ.trend.percentage == pytest.approx(2.0)

    # 2. Revenue widget
    w_rev = WidgetService.build_revenue_widget(12000.0, 150.0, 110.0, 5.0, [100, 110])
    assert w_rev.id == "widget-revenue"
    assert w_rev.value["adr"] == "$150.00"

    # 3. Forecast widget
    w_fc = WidgetService.build_forecast_widget([0.7, 0.8], ["Mon", "Tue"])
    assert w_fc.id == "widget-forecast"
    assert w_fc.widget_type == WidgetType.BAR_CHART

    # 4. Health widget
    w_h = WidgetService.build_health_widget(88.5)
    assert w_h.id == "widget-health"
    assert w_h.status == WidgetStatus.HEALTHY

    # 5. Room status widget
    w_room = WidgetService.build_room_status_widget(45, 10, 5)
    assert w_room.id == "widget-room-status"

    # 6. Operations widget
    w_ops = WidgetService.build_operations_widget(0.92, 15)
    assert w_ops.id == "widget-operations"

    # 7. Guest widget
    w_guest = WidgetService.build_guest_satisfaction_widget(4.6, 2.5)
    assert w_guest.id == "widget-guest-satisfaction"


def test_business_health_score_calculation() -> None:
    # Test high values
    score_high = ExecutiveService.calculate_health_score(0.90, 210.0, 0.95, 4.8, 1)
    assert score_high >= 85.0
    assert score_high <= 100.0

    # Test low values
    score_low = ExecutiveService.calculate_health_score(0.30, 80.0, 0.50, 2.8, 10)
    assert score_low < 50.0


def test_layout_role_mapping() -> None:
    lay_exec = LayoutService.get_layout_for_role("Executive")
    assert lay_exec["columns"] == 12
    assert any(w["widget_id"] == "widget-health" for w in lay_exec["widgets"])

    lay_rev = LayoutService.get_layout_for_role("Revenue Manager")
    assert any(w["widget_id"] == "widget-forecast" for w in lay_rev["widgets"])

    lay_ops = LayoutService.get_layout_for_role("Operations Manager")
    assert any(w["widget_id"] == "widget-room-status" for w in lay_ops["widgets"])

    lay_staff = LayoutService.get_layout_for_role("Staff")
    assert len(lay_staff["widgets"]) == 2


def test_alert_engine_thresholds() -> None:
    engine = AlertEngine()

    # Trigger all alerts by feeding poor metric bounds
    alerts = engine.evaluate_thresholds(
        occupancy_forecast_7d=[0.35] * 7,
        daily_revenues=[1000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0, 2000.0],
        cancellations_today=6,
        unassigned_critical_maintenance=3,
        turnaround_sla_compliance=0.85,
        avg_guest_satisfaction=3.2,
        forecasting_model_drift=0.35,
        rag_confidence=0.15,
    )

    assert len(alerts) == 8
    # Assert specific details
    assert any(a.title == "Low Forecasted Occupancy" for a in alerts)
    assert any(a.title == "Significant Revenue Drop" for a in alerts)
    assert any(a.title == "Spike in Booking Cancellations" for a in alerts)
    assert any(a.title == "Critical Maintenance Backlog" for a in alerts)
    assert any(a.title == "Housekeeping Turnaround SLA Failure" for a in alerts)
    assert any(a.title == "Poor Guest Satisfaction Ratings" for a in alerts)
    assert any(a.title == "Model Drift Alert" for a in alerts)
    assert any(a.title == "Knowledge Retrieval Failure" for a in alerts)


def test_sliced_analytics() -> None:
    # Test Housekeeping slice
    res_hk = AnalyticsService.get_sliced_analytics(department="housekeeping")
    assert res_hk["kpis"]["operational_tasks"] == 320

    # Test Suite slice
    res_suite = AnalyticsService.get_sliced_analytics(room_type="Deluxe Suite")
    assert res_suite["kpis"]["revenue"] == 92000.00

    # Test segment Corporate slice
    res_corp = AnalyticsService.get_sliced_analytics(guest_segment="corporate")
    assert res_corp["kpis"]["guest_satisfaction_rating"] == 4.4


def test_forecast_payload() -> None:
    res = DashboardForecastingService.get_forecast_payload(
        horizon_days=15, compare_historical=True
    )
    assert len(res["data_points"]) == 15
    assert len(res["anomalies"]) == 1
    assert "historical_occupancy" in res["data_points"][0]


def test_export_engine() -> None:
    json_bytes = ExportEngine.export_dataset("JSON", "EXECUTIVE", {})
    assert b"dataset_type" in json_bytes

    csv_bytes = ExportEngine.export_dataset("CSV", "REVENUE", {})
    assert b"Metric,Value,Status" in csv_bytes

    excel_bytes = ExportEngine.export_dataset("EXCEL", "OPERATIONS", {})
    assert b"Metric\tValue\tStatus" in excel_bytes

    pdf_bytes = ExportEngine.export_dataset("PDF", "GUESTS", {})
    assert pdf_bytes.startswith(b"%PDF-1.4")


@pytest.mark.asyncio
async def test_ai_report_compilation() -> None:
    # Test fallback flow
    engine = AIReportingEngine()
    report = await engine.generate_report(interval="WEEKLY", department="ALL")
    assert isinstance(report, AIReportPackage)
    assert len(report.ai_insights) == 2
    assert report.kpis["occupancy"] == 0.74

    # Test with mock services
    mock_ai = MagicMock(spec=AIService)
    mock_ai.generate = AsyncMock()
    mock_ai.generate.return_value.content = (
        "Insight: High peak revenue\nRec: Adjust weekend rates"
    )

    mock_retriever = MagicMock(spec=Retriever)
    mock_retriever.retrieve = AsyncMock()
    mock_retriever.retrieve.return_value = [
        MagicMock(text="Custom housekeeping threshold 30m")
    ]

    engine_mocked = AIReportingEngine(ai_service=mock_ai, retriever=mock_retriever)
    report_mocked = await engine_mocked.generate_report(
        interval="DAILY", department="REVENUE"
    )
    assert "High peak revenue" in report_mocked.ai_insights
    assert report_mocked.recommendations[0]["description"] == "Adjust weekend rates"


@pytest.mark.asyncio
async def test_executive_assistant_agent() -> None:
    mock_ai = MagicMock(spec=AIService)
    mock_ai.generate = AsyncMock()
    mock_ai.generate.return_value.content = (
        "Synthetic response explaining occupancy drop"
    )

    mock_retriever = MagicMock(spec=Retriever)
    mock_retriever.retrieve = AsyncMock()
    mock_retriever.retrieve.return_value = [
        MagicMock(text="Retrieved policy document: markup limit is 30%")
    ]

    agent = ExecutiveAssistantAgent(ai_service=mock_ai, retriever=mock_retriever)
    res = await agent.ask_question("Why is occupancy lower this week?")
    assert "Synthetic response" in res["response"]
    assert "revenue-service" in res["citations"]
