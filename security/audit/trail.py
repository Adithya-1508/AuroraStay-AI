import hashlib
from datetime import UTC, datetime
from typing import Any


class AuditTrail:
    """Manages append-only, tamper-evident log records of privileged operations."""

    def __init__(self) -> None:
        self.logs: list[dict[str, Any]] = []
        self._last_hash = "0" * 64

    def log_action(
        self, identity_id: str, action: str, resource: str, status: str, ip: str
    ) -> dict[str, Any]:
        """Appends an operation audit record and updates the cryptographic hash chain."""
        timestamp = datetime.now(UTC).isoformat()
        payload = f"{timestamp}|{identity_id}|{action}|{resource}|{status}|{ip}|{self._last_hash}"
        new_hash = hashlib.sha256(payload.encode()).hexdigest()

        entry = {
            "audit_id": f"aud-{hashlib.sha256(new_hash.encode()).hexdigest()[:8]}",
            "timestamp": timestamp,
            "identity_id": identity_id,
            "action": action,
            "resource": resource,
            "status": status,
            "ip_address": ip,
            "hash": new_hash,
            "previous_hash": self._last_hash,
        }

        self.logs.append(entry)
        self._last_hash = new_hash
        return entry

    def verify_chain_integrity(self) -> bool:
        """Validates the integrity of the audit logs to detect deletions or modifications."""
        current_prev_hash = "0" * 64
        for log in self.logs:
            if log["previous_hash"] != current_prev_hash:
                return False
            payload = f"{log['timestamp']}|{log['identity_id']}|{log['action']}|{log['resource']}|{log['status']}|{log['ip_address']}|{current_prev_hash}"
            expected_hash = hashlib.sha256(payload.encode()).hexdigest()
            if log["hash"] != expected_hash:
                return False
            current_prev_hash = log["hash"]
        return True
