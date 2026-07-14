from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel


class SecurityIncident(BaseModel):
    incident_id: str
    title: str
    severity: str  # CRITICAL | HIGH | MEDIUM | LOW
    source_ip: str
    status: str  # OPEN | INVESTIGATING | CONTAINED | RESOLVED
    containment_action: str | None = None
    linked_audit_ids: list[str] = []
    created_at: datetime


class SecurityIncidentTracker:
    """Manages tracking, indexing, and containment procedures for security incidents."""

    def __init__(self) -> None:
        self.incidents: dict[str, SecurityIncident] = {}

    def log_incident(
        self,
        title: str,
        severity: str,
        source_ip: str,
        linked_audits: list[str],
    ) -> SecurityIncident:
        inc_id = f"sec-inc-{uuid4().hex[:8]}"
        incident = SecurityIncident(
            incident_id=inc_id,
            title=title,
            severity=severity,
            source_ip=source_ip,
            status="OPEN",
            linked_audit_ids=linked_audits,
            created_at=datetime.now(UTC),
        )
        self.incidents[inc_id] = incident
        return incident

    def update_containment(
        self, incident_id: str, action: str, status: str
    ) -> SecurityIncident | None:
        if incident_id in self.incidents:
            inc = self.incidents[incident_id]
            inc.containment_action = action
            inc.status = status
            return inc
        return None

    def list_incidents(self) -> list[SecurityIncident]:
        return list(self.incidents.values())
