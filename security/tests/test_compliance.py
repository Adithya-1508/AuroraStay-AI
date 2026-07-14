from security.administration.console import AdminConsole
from security.audit.trail import AuditTrail
from security.compliance.purge import GDPRComplianceManager
from security.risk.evaluator import RiskEvaluator


def test_audit_integrity_blockchain() -> None:
    trail = AuditTrail()

    # Log operations
    trail.log_action("usr-1", "CREATE_RESERVATION", "res-1", "SUCCESS", "127.0.0.1")
    trail.log_action("usr-1", "DELETE_RESERVATION", "res-1", "SUCCESS", "127.0.0.1")

    # Verify integrity passes
    assert trail.verify_chain_integrity() is True

    # Tamper with log context
    trail.logs[0]["action"] = "UNAUTHORIZED_ACTION"
    assert trail.verify_chain_integrity() is False

    # Restore action and tamper with previous hash
    trail.logs[0]["action"] = "CREATE_RESERVATION"
    trail.logs[1]["previous_hash"] = "tampered_hash"
    assert trail.verify_chain_integrity() is False


def test_gdpr_pii_purge_compliance() -> None:
    guest_profile = {
        "guest_id": "gst-1",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@email.com",
        "phone": "555-123-4567",
        "loyalty_tier": "Gold",
    }
    purged = GDPRComplianceManager.purge_guest_pii(guest_profile)
    assert purged["first_name"] == "ANONYMIZED"
    assert purged["email"] == "anonymized@gdpr.hospitalityai.local"
    assert purged["loyalty_tier"] == "Gold"  # non-PII metrics retained


def test_admin_approvals_console() -> None:
    console = AdminConsole()
    assert console.maintenance_mode is False

    # Toggle maintenance mode
    console.set_maintenance_mode(True)
    assert console.maintenance_mode is True

    # AI Approvals gates checks
    assert console.is_model_approved("forecaster-v1") is False
    console.register_model_approval("forecaster-v1", "APPROVED")
    assert console.is_model_approved("forecaster-v1") is True

    assert console.is_prompt_approved("pricing_explanation") is False
    console.register_prompt_approval("pricing_explanation", "APPROVED")
    assert console.is_prompt_approved("pricing_explanation") is True


def test_risk_evaluations() -> None:
    # 1. Low risk
    score_low = RiskEvaluator.calculate_request_risk(0, 0, 0)
    assert RiskEvaluator.get_risk_label(score_low) == "LOW"

    # 2. Medium risk
    score_med = RiskEvaluator.calculate_request_risk(2, 0, 0)
    assert RiskEvaluator.get_risk_label(score_med) == "MEDIUM"

    # 3. High risk
    score_high = RiskEvaluator.calculate_request_risk(3, 0, 1)
    assert RiskEvaluator.get_risk_label(score_high) == "HIGH"

    # 4. Critical risk (due to injection flags)
    score_crit = RiskEvaluator.calculate_request_risk(0, 1, 0)
    assert RiskEvaluator.get_risk_label(score_crit) == "CRITICAL"


def test_security_incident_tracking() -> None:
    from security.incident_response.tracker import SecurityIncidentTracker

    tracker = SecurityIncidentTracker()
    inc = tracker.log_incident("Compromised Key", "HIGH", "127.0.0.1", ["aud-test"])
    assert inc.status == "OPEN"

    res = tracker.update_containment(inc.incident_id, "Suspended Key", "CONTAINED")
    assert res is not None
    assert res.status == "CONTAINED"
    assert res.containment_action == "Suspended Key"

    # Invalid ID check
    assert tracker.update_containment("invalid-id", "action", "status") is None
