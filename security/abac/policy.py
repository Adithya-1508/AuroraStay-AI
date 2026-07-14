from datetime import datetime, time


class ABACPolicyEngine:
    """Evaluates request context attributes (IPs, time-windows, department scopes)."""

    # Blacklisted IP ranges
    IP_BLACKLIST = {"192.168.1.99", "10.0.0.99"}

    # Allowed operational hours: 06:00:00 to 22:00:00
    OPERATIONAL_START = time(6, 0)
    OPERATIONAL_END = time(22, 0)

    @classmethod
    def evaluate_context(
        cls,
        client_ip: str,
        user_dept: str,
        resource_dept: str,
        current_time: time | None = None,
    ) -> bool:
        """Enforces shift windows, client IP restrictions, and department isolation."""
        # 1. IP Blacklist check
        if client_ip in cls.IP_BLACKLIST:
            return False

        # 2. Operational shift time check
        check_time = current_time or datetime.utcnow().time()
        if not (cls.OPERATIONAL_START <= check_time <= cls.OPERATIONAL_END):
            # Block administrative/operational modifications outside operational hours
            # Exception for general/IT managers if needed, but restrict by default
            if user_dept in [
                "Housekeeping",
                "Maintenance",
                "Receptionist",
                "Reception",
            ]:
                return False

        # 3. Department isolation (users can only access resource of their own department,
        # unless user_dept is 'ALL' or 'Administration')
        if user_dept != "ALL" and user_dept != "Administration":
            if resource_dept != "ALL" and user_dept != resource_dept:
                return False

        return True
