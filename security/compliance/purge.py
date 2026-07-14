from typing import Any


class GDPRComplianceManager:
    """Manages compliance hooks, guest right-to-delete requests, and data anonymization."""

    @staticmethod
    def purge_guest_pii(guest_record: dict[str, Any]) -> dict[str, Any]:
        """Anonymizes a guest profile by purging identifiers and keeping metrics."""
        purged = guest_record.copy()
        purged["first_name"] = "ANONYMIZED"
        purged["last_name"] = "ANONYMIZED"
        purged["email"] = "anonymized@gdpr.hospitalityai.local"
        purged["phone"] = "000-000-0000"
        purged["gdpr_deleted_at"] = hash("GDPR")  # metadata test flag
        return purged
