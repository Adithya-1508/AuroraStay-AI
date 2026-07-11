from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel


class AlertSeverity(str, Enum):  # noqa: UP042
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class Alert(BaseModel):
    id: str
    title: str
    severity: AlertSeverity
    reason: str
    suggested_actions: list[str]
    owner: str
    triggered_at: datetime
    is_acknowledged: bool = False


class AlertEngine:
    """Evaluates hotel KPIs against defined operational limits to trigger alerts."""

    def __init__(self) -> None:
        self.alerts: list[Alert] = []

    def clear_alerts(self) -> None:
        self.alerts = []

    def evaluate_thresholds(
        self,
        occupancy_forecast_7d: list[float],
        daily_revenues: list[float],  # last 8 days [yesterday, day-2, ...]
        cancellations_today: int,
        unassigned_critical_maintenance: int,
        turnaround_sla_compliance: float,
        avg_guest_satisfaction: float,
        forecasting_model_drift: float,
        rag_confidence: float,
    ) -> list[Alert]:
        """Runs threshold checks across platforms and populates active alerts."""
        self.clear_alerts()
        now = datetime.now(UTC)

        # 1. Low Occupancy Check (forecast < 40%)
        if occupancy_forecast_7d:
            avg_occ = sum(occupancy_forecast_7d) / len(occupancy_forecast_7d)
            if avg_occ < 0.40:
                self.alerts.append(
                    Alert(
                        id=f"alert-occ-{uuid4().hex[:8]}",
                        title="Low Forecasted Occupancy",
                        severity=AlertSeverity.CRITICAL,
                        reason=f"7-day average forecasted occupancy is {avg_occ * 100:.1f}% (Threshold: <40.0%)",
                        suggested_actions=[
                            "Deploy dynamic price discounts to spark demand",
                            "Initiate targeting email campaign to loyalty segments",
                        ],
                        owner="Revenue Manager",
                        triggered_at=now,
                    )
                )

        # 2. Revenue Drop Check (yesterday's revenue drop > 20% compared to 7-day average)
        if len(daily_revenues) >= 8:
            yesterday_rev = daily_revenues[0]
            avg_7d = sum(daily_revenues[1:8]) / 7
            if avg_7d > 0:
                drop_pct = (avg_7d - yesterday_rev) / avg_7d
                if drop_pct > 0.20:
                    self.alerts.append(
                        Alert(
                            id=f"alert-rev-{uuid4().hex[:8]}",
                            title="Significant Revenue Drop",
                            severity=AlertSeverity.CRITICAL,
                            reason=f"Yesterday's revenue drop is {drop_pct * 100:.1f}% vs 7-day average (Threshold: >20.0%)",
                            suggested_actions=[
                                "Review ADR levels and competitor rates",
                                "Verify upsell and cross-sell engine health",
                            ],
                            owner="Revenue Manager",
                            triggered_at=now,
                        )
                    )

        # 3. High Cancellations Check (> 5 cancellations)
        if cancellations_today > 5:
            self.alerts.append(
                Alert(
                    id=f"alert-cnc-{uuid4().hex[:8]}",
                    title="Spike in Booking Cancellations",
                    severity=AlertSeverity.WARNING,
                    reason=f"Recorded {cancellations_today} cancellations today (Threshold: >5)",
                    suggested_actions=[
                        "Investigate recent policy updates",
                        "Evaluate cancellation patterns by booking channel",
                    ],
                    owner="Reservations Manager",
                    triggered_at=now,
                )
            )

        # 4. Maintenance Backlog Check (Critical unassigned > 0)
        if unassigned_critical_maintenance > 0:
            self.alerts.append(
                Alert(
                    id=f"alert-mnt-{uuid4().hex[:8]}",
                    title="Critical Maintenance Backlog",
                    severity=AlertSeverity.CRITICAL,
                    reason=f"Found {unassigned_critical_maintenance} critical maintenance tasks unassigned",
                    suggested_actions=[
                        "Dispatch operations supervisor to assign tasks",
                        "Escalate tasks to external service providers",
                    ],
                    owner="Operations Manager",
                    triggered_at=now,
                )
            )

        # 5. SLA Turnaround Violations (turnaround SLA compliance < 90%)
        if turnaround_sla_compliance < 0.90:
            self.alerts.append(
                Alert(
                    id=f"alert-sla-{uuid4().hex[:8]}",
                    title="Housekeeping Turnaround SLA Failure",
                    severity=AlertSeverity.WARNING,
                    reason=f"Housekeeping SLA compliance dropped to {turnaround_sla_compliance * 100:.1f}% (Threshold: <90.0%)",
                    suggested_actions=[
                        "Optimize staff allocation for checkout peaks",
                        "Identify room type bottlenecks causing delays",
                    ],
                    owner="Operations Manager",
                    triggered_at=now,
                )
            )

        # 6. Poor Guest Satisfaction (score < 3.5)
        if avg_guest_satisfaction < 3.5:
            self.alerts.append(
                Alert(
                    id=f"alert-gst-{uuid4().hex[:8]}",
                    title="Poor Guest Satisfaction Ratings",
                    severity=AlertSeverity.CRITICAL,
                    reason=f"Average guest sentiment score is {avg_guest_satisfaction:.1f}/5.0 (Threshold: <3.5)",
                    suggested_actions=[
                        "Retrieve conversational complaint context via Assistant",
                        "Conduct courtesy calls or offer loyalty offsets to affected guests",
                    ],
                    owner="Guest Experience Manager",
                    triggered_at=now,
                )
            )

        # 7. Model Degradation (drift > 0.25)
        if forecasting_model_drift > 0.25:
            self.alerts.append(
                Alert(
                    id=f"alert-drf-{uuid4().hex[:8]}",
                    title="Model Drift Alert",
                    severity=AlertSeverity.WARNING,
                    reason=f"Active forecasting model drift score is {forecasting_model_drift:.2f} (Threshold: >0.25)",
                    suggested_actions=[
                        "Trigger model retraining pipeline immediately",
                        "Rollback model registry status to last stable version",
                    ],
                    owner="Revenue Manager",
                    triggered_at=now,
                )
            )

        # 8. Knowledge Failures (RAG confidence < 0.3)
        if rag_confidence < 0.3:
            self.alerts.append(
                Alert(
                    id=f"alert-rag-{uuid4().hex[:8]}",
                    title="Knowledge Retrieval Failure",
                    severity=AlertSeverity.INFO,
                    reason=f"Knowledge retrieval query confidence is {rag_confidence:.2f} (Threshold: <0.30)",
                    suggested_actions=[
                        "Review policy document formatting and indices",
                        "Verify Qdrant vector database storage and alignment",
                    ],
                    owner="Executive Assistant Agent",
                    triggered_at=now,
                )
            )

        return self.alerts
