from observability.governance.privacy import PIIRedactor
from observability.governance.registry import GovernanceRegistry


def test_pii_redaction() -> None:
    # Redact email
    text_email = "Please contact me at admin@hotel.com"
    assert "admin@hotel.com" not in PIIRedactor.redact_text(text_email)
    assert "[REDACTED_EMAIL]" in PIIRedactor.redact_text(text_email)

    # Redact phone
    text_phone = "My phone number is 123-456-7890."
    assert "123-456-7890" not in PIIRedactor.redact_text(text_phone)
    assert "[REDACTED_PHONE]" in PIIRedactor.redact_text(text_phone)


def test_governance_registry() -> None:
    reg = GovernanceRegistry()

    # Verify registered default assets
    assert reg.verify_asset_compliance("model", "forecaster-regressor")
    assert reg.verify_asset_compliance("prompt", "pricing_explanation")
    assert reg.verify_asset_compliance("agent", "GuestConcierge")

    # Verify registering new models
    reg.register_model(
        "recommendation-collaboration", "Revenue Team", "HIGH", "PII_REDACTED"
    )
    assert reg.verify_asset_compliance("model", "recommendation-collaboration")

    # Verify unregistered asset fails
    assert not reg.verify_asset_compliance("model", "unregistered-v1")
    assert not reg.verify_asset_compliance("unsupported_type", "GuestConcierge")
