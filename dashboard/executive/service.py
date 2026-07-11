from typing import Any

from dashboard.alerts.engine import AlertEngine
from dashboard.widgets.service import WidgetService


class ExecutiveService:
    """Orchestrates general overview KPI calculations and widget listings."""

    @staticmethod
    def calculate_health_score(
        occupancy_rate: float,
        adr: float,
        sla_compliance: float,
        guest_satisfaction: float,
        cancellations_today: int,
    ) -> float:
        """Computes business health score out of 100 based on core metrics."""
        w1, w2, w3, w4, w5 = 30, 25, 20, 25, 10

        adr_norm = min(adr / 200.0, 1.0)
        gs_norm = min(guest_satisfaction / 5.0, 1.0)

        score = (
            w1 * occupancy_rate
            + w2 * adr_norm
            + w3 * sla_compliance
            + w4 * gs_norm
            - w5 * min(cancellations_today * 0.1, 1.0)
        )
        return max(min(score, 100.0), 0.0)

    def get_overview(
        self,
        occupancy_rate: float,
        last_month_occupancy: float,
        today_arrivals: int,
        today_departures: int,
        total_billing: float,
        adr: float,
        revpar: float,
        trend_percentage: float,
        sparkline: list[float],
        forecast_occupancy: list[float],
        forecast_labels: list[str],
        clean_rooms: int,
        dirty_rooms: int,
        in_progress_rooms: int,
        sla_compliance: float,
        pending_tasks: int,
        avg_guest_satisfaction: int | float,
        cancellations_today: int,
        model_drift: float = 0.0,
        rag_confidence: float = 0.9,
    ) -> dict[str, Any]:
        """Synthesizes overview payload, active widgets, and alerts."""
        health = self.calculate_health_score(
            occupancy_rate,
            adr,
            sla_compliance,
            float(avg_guest_satisfaction),
            cancellations_today,
        )

        # Trigger Alerts
        alert_engine = AlertEngine()
        alerts = alert_engine.evaluate_thresholds(
            occupancy_forecast_7d=forecast_occupancy[:7],
            daily_revenues=[total_billing / 7] * 8,  # mock last 8 days
            cancellations_today=cancellations_today,
            unassigned_critical_maintenance=dirty_rooms,  # using dirty rooms as mock indicator
            turnaround_sla_compliance=sla_compliance,
            avg_guest_satisfaction=float(avg_guest_satisfaction),
            forecasting_model_drift=model_drift,
            rag_confidence=rag_confidence,
        )

        # Build standard widgets list
        widgets = [
            WidgetService.build_health_widget(health),
            WidgetService.build_occupancy_widget(occupancy_rate, last_month_occupancy),
            WidgetService.build_guest_satisfaction_widget(
                float(avg_guest_satisfaction), trend_percentage
            ),
            WidgetService.build_revenue_widget(
                total_billing, adr, revpar, trend_percentage, sparkline
            ),
            WidgetService.build_forecast_widget(forecast_occupancy, forecast_labels),
            WidgetService.build_room_status_widget(
                clean_rooms, dirty_rooms, in_progress_rooms
            ),
            WidgetService.build_operations_widget(sla_compliance, pending_tasks),
            WidgetService.build_alerts_widget(alerts),
        ]

        # Recommendations list (Mock for dashboard view)
        ai_recommendations = [
            {
                "id": "rec-1",
                "action": "Offer suite upgrade to incoming Gold tier guests",
                "reason": "7 Deluxe suites vacant with 5 arrivals having high upsell probability",
                "expected_impact": "+$850 revenue",
                "confidence": 0.92,
            },
            {
                "id": "rec-2",
                "action": "Increase spa cross-sell promotions by 10% on weekends",
                "reason": "High weekend guest volume with lower historical spa bookings",
                "expected_impact": "+$1,500 revenue",
                "confidence": 0.88,
            },
        ]

        return {
            "business_health_score": health,
            "metrics": {
                "current_occupancy": occupancy_rate,
                "today_arrivals": today_arrivals,
                "today_departures": today_departures,
                "current_revenue": total_billing,
                "forecasted_occupancy_30d": sum(forecast_occupancy)
                / max(len(forecast_occupancy), 1),
                "forecasted_revenue_30d": total_billing * 4.3,  # estimated monthly
                "outstanding_tasks": pending_tasks,
                "critical_alerts_count": len(
                    [a for a in alerts if a.severity == "CRITICAL"]
                ),
            },
            "widgets": [w.model_dump() for w in widgets],
            "ai_recommendations": ai_recommendations,
            "alerts": [a.model_dump() for a in alerts],
        }
