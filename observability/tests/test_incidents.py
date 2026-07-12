from observability.incidents.service import (
    IncidentService,
    IncidentSeverity,
    IncidentStatus,
)


def test_incident_lifecyle() -> None:
    service = IncidentService()

    # 1. Create incident
    inc = service.create_incident(
        title="Housekeeping SLA Breach",
        severity=IncidentSeverity.CRITICAL,
        source="WORKFLOW",
        root_cause="Housekeeper staff utilization gap",
    )
    assert inc.status == IncidentStatus.OPEN
    assert inc.severity == IncidentSeverity.CRITICAL
    assert len(inc.timeline) == 1

    # 2. Add event
    service.add_timeline_event(inc.incident_id, "Operations manager notified")
    assert len(inc.timeline) == 2

    # 3. Resolve incident
    res = service.resolve_incident(
        incident_id=inc.incident_id,
        resolution="Re-scheduled shift hours",
        lessons_learned="Buffer weekend housekeeper counts",
    )
    assert res is not None
    assert res.status == IncidentStatus.RESOLVED
    assert res.lessons_learned == "Buffer weekend housekeeper counts"
    assert len(res.timeline) == 3

    # 4. List incidents
    incidents = service.list_incidents("RESOLVED")
    assert len(incidents) == 1

    # 5. Invalid resolution check
    assert service.resolve_incident("invalid-id", "res", "lesson") is None
