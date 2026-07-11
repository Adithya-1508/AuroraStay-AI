from enum import Enum
from typing import Any

from pydantic import BaseModel


class WidgetType(str, Enum):  # noqa: UP042
    VALUE = "VALUE"
    SPARKLINE = "SPARKLINE"
    BAR_CHART = "BAR_CHART"
    PIE_CHART = "PIE_CHART"
    TABLE = "TABLE"
    LIST = "LIST"


class WidgetTrendDirection(str, Enum):  # noqa: UP042
    UP = "UP"
    DOWN = "DOWN"
    STABLE = "STABLE"


class WidgetStatus(str, Enum):  # noqa: UP042
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class WidgetTrend(BaseModel):
    direction: WidgetTrendDirection
    percentage: float
    label: str


class WidgetMetadata(BaseModel):
    department: str
    size: str


class Widget(BaseModel):
    id: str
    title: str
    widget_type: WidgetType
    value: Any
    trend: WidgetTrend | None = None
    sparkline_data: list[float] | None = None
    status: WidgetStatus = WidgetStatus.HEALTHY
    metadata: WidgetMetadata


class WidgetService:
    """Service to instantiate and standardize reusable dashboard widgets."""

    @staticmethod
    def build_occupancy_widget(
        occupancy_rate: float, last_month_occupancy: float
    ) -> Widget:
        diff = occupancy_rate - last_month_occupancy
        direction = (
            WidgetTrendDirection.UP
            if diff > 0.001
            else (
                WidgetTrendDirection.DOWN
                if diff < -0.001
                else WidgetTrendDirection.STABLE
            )
        )
        status = (
            WidgetStatus.HEALTHY
            if occupancy_rate >= 0.70
            else (
                WidgetStatus.WARNING
                if occupancy_rate >= 0.50
                else WidgetStatus.CRITICAL
            )
        )
        return Widget(
            id="widget-occupancy",
            title="Current Occupancy Rate",
            widget_type=WidgetType.VALUE,
            value=f"{occupancy_rate * 100:.1f}%",
            trend=WidgetTrend(
                direction=direction,
                percentage=abs(diff) * 100,
                label="vs last month",
            ),
            status=status,
            metadata=WidgetMetadata(department="Reservations", size="SMALL"),
        )

    @staticmethod
    def build_revenue_widget(
        total_billing: float,
        adr: float,
        revpar: float,
        trend_percentage: float,
        sparkline: list[float],
    ) -> Widget:
        direction = (
            WidgetTrendDirection.UP
            if trend_percentage > 0.1
            else (
                WidgetTrendDirection.DOWN
                if trend_percentage < -0.1
                else WidgetTrendDirection.STABLE
            )
        )
        return Widget(
            id="widget-revenue",
            title="Revenue & Performance Indicators",
            widget_type=WidgetType.SPARKLINE,
            value={
                "total_billing": f"${total_billing:,.2f}",
                "adr": f"${adr:,.2f}",
                "revpar": f"${revpar:,.2f}",
            },
            trend=WidgetTrend(
                direction=direction,
                percentage=abs(trend_percentage),
                label="vs previous week",
            ),
            sparkline_data=sparkline,
            status=WidgetStatus.HEALTHY,
            metadata=WidgetMetadata(department="Revenue", size="MEDIUM"),
        )

    @staticmethod
    def build_forecast_widget(
        forecast_occupancy: list[float], labels: list[str]
    ) -> Widget:
        # standard 7-day or 30-day visual forecast
        avg_fc = sum(forecast_occupancy) / max(len(forecast_occupancy), 1)
        status = WidgetStatus.HEALTHY if avg_fc >= 0.65 else WidgetStatus.WARNING
        return Widget(
            id="widget-forecast",
            title="30-Day Occupancy Forecast",
            widget_type=WidgetType.BAR_CHART,
            value={
                "labels": labels,
                "dataset": forecast_occupancy,
            },
            status=status,
            metadata=WidgetMetadata(department="Revenue", size="LARGE"),
        )

    @staticmethod
    def build_health_widget(health_score: float) -> Widget:
        status = (
            WidgetStatus.HEALTHY
            if health_score >= 85
            else (WidgetStatus.WARNING if health_score >= 70 else WidgetStatus.CRITICAL)
        )
        return Widget(
            id="widget-health",
            title="Business Health Score",
            widget_type=WidgetType.VALUE,
            value=f"{health_score:.1f}/100",
            status=status,
            metadata=WidgetMetadata(department="Executive", size="SMALL"),
        )

    @staticmethod
    def build_room_status_widget(clean: int, dirty: int, in_progress: int) -> Widget:
        total = clean + dirty + in_progress
        dirty_pct = (dirty / total * 100) if total > 0 else 0
        status = (
            WidgetStatus.CRITICAL
            if dirty_pct >= 40
            else (WidgetStatus.WARNING if dirty_pct >= 20 else WidgetStatus.HEALTHY)
        )
        return Widget(
            id="widget-room-status",
            title="Room Turnaround Status",
            widget_type=WidgetType.PIE_CHART,
            value={
                "clean": clean,
                "dirty": dirty,
                "in_progress": in_progress,
            },
            status=status,
            metadata=WidgetMetadata(department="Operations", size="SMALL"),
        )

    @staticmethod
    def build_alerts_widget(alerts: list[Any]) -> Widget:
        critical_count = sum(
            1 for a in alerts if getattr(a, "severity", "") == "CRITICAL"
        )
        status = (
            WidgetStatus.CRITICAL
            if critical_count > 0
            else (WidgetStatus.WARNING if len(alerts) > 0 else WidgetStatus.HEALTHY)
        )
        return Widget(
            id="widget-alerts",
            title="Critical Operating Alerts",
            widget_type=WidgetType.LIST,
            value=alerts,
            status=status,
            metadata=WidgetMetadata(department="Executive", size="MEDIUM"),
        )

    @staticmethod
    def build_operations_widget(sla_compliance: float, pending_tasks: int) -> Widget:
        status = (
            WidgetStatus.HEALTHY
            if sla_compliance >= 0.90
            else (
                WidgetStatus.WARNING
                if sla_compliance >= 0.75
                else WidgetStatus.CRITICAL
            )
        )
        return Widget(
            id="widget-operations",
            title="Operations SLA Compliance",
            widget_type=WidgetType.VALUE,
            value=f"{sla_compliance * 100:.1f}%",
            trend=WidgetTrend(
                direction=WidgetTrendDirection.STABLE,
                percentage=0.0,
                label=f"{pending_tasks} outstanding tasks",
            ),
            status=status,
            metadata=WidgetMetadata(department="Operations", size="SMALL"),
        )

    @staticmethod
    def build_guest_satisfaction_widget(
        satisfaction_score: float, trend_percentage: float
    ) -> Widget:
        direction = (
            WidgetTrendDirection.UP
            if trend_percentage > 0.1
            else (
                WidgetTrendDirection.DOWN
                if trend_percentage < -0.1
                else WidgetTrendDirection.STABLE
            )
        )
        status = (
            WidgetStatus.HEALTHY
            if satisfaction_score >= 4.2
            else (
                WidgetStatus.WARNING
                if satisfaction_score >= 3.5
                else WidgetStatus.CRITICAL
            )
        )
        return Widget(
            id="widget-guest-satisfaction",
            title="Guest Satisfaction Score",
            widget_type=WidgetType.VALUE,
            value=f"{satisfaction_score:.1f}/5.0",
            trend=WidgetTrend(
                direction=direction,
                percentage=abs(trend_percentage),
                label="vs previous week",
            ),
            status=status,
            metadata=WidgetMetadata(department="Guests", size="SMALL"),
        )
