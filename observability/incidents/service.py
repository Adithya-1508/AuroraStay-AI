from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel


class IncidentSeverity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(StrEnum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"


class IncidentTimelineEvent(BaseModel):
    timestamp: datetime
    event: str


class Incident(BaseModel):
    incident_id: str
    title: str
    severity: IncidentSeverity
    source: str
    root_cause: str
    status: IncidentStatus = IncidentStatus.OPEN
    timeline: list[IncidentTimelineEvent]
    resolution: str | None = None
    lessons_learned: str | None = None


class IncidentService:
    """Manages AI incidents and tracks root cause logs and timelines."""

    def __init__(self) -> None:
        self.incidents: dict[str, Incident] = {}

    def create_incident(
        self, title: str, severity: IncidentSeverity, source: str, root_cause: str
    ) -> Incident:
        inc_id = f"inc-{uuid4().hex[:8]}"
        now = datetime.now(UTC)

        incident = Incident(
            incident_id=inc_id,
            title=title,
            severity=severity,
            source=source,
            root_cause=root_cause,
            timeline=[
                IncidentTimelineEvent(
                    timestamp=now,
                    event=f"Incident ticket opened automatically: {title}",
                )
            ],
        )
        self.incidents[inc_id] = incident
        return incident

    def add_timeline_event(self, incident_id: str, event_text: str) -> None:
        if incident_id in self.incidents:
            self.incidents[incident_id].timeline.append(
                IncidentTimelineEvent(
                    timestamp=datetime.now(UTC),
                    event=event_text,
                )
            )

    def resolve_incident(
        self, incident_id: str, resolution: str, lessons_learned: str
    ) -> Incident | None:
        if incident_id in self.incidents:
            inc = self.incidents[incident_id]
            inc.status = IncidentStatus.RESOLVED
            inc.resolution = resolution
            inc.lessons_learned = lessons_learned
            inc.timeline.append(
                IncidentTimelineEvent(
                    timestamp=datetime.now(UTC),
                    event=f"Incident resolved: {resolution}",
                )
            )
            return inc
        return None

    def list_incidents(self, status: str | None = None) -> list[Incident]:
        inc_list = list(self.incidents.values())
        if status:
            return [i for i in inc_list if i.status == status]
        return inc_list
