class PermissionEngine:
    """Evaluates scoped permissions and checks against allowed user roles."""

    # Resource -> roles mapping
    PERMISSION_ROLES = {
        "reservation:read": [
            "Guest",
            "Receptionist",
            "Operations Manager",
            "General Manager",
            "Administrator",
        ],
        "reservation:write": [
            "Receptionist",
            "Operations Manager",
            "General Manager",
            "Administrator",
        ],
        "housekeeping:read": [
            "Housekeeping",
            "Operations Manager",
            "General Manager",
            "Administrator",
        ],
        "housekeeping:write": ["Housekeeping", "Operations Manager", "Administrator"],
        "revenue:read": [
            "Revenue Manager",
            "Operations Manager",
            "General Manager",
            "Administrator",
        ],
        "revenue:write": ["Revenue Manager", "Administrator"],
        "audit:read": ["Auditor", "Administrator", "System Administrator"],
        "model:approve": ["AI Administrator", "ML Engineer", "System Administrator"],
    }

    @classmethod
    def check_permission(
        cls, assigned_roles: list[str], required_permission: str
    ) -> bool:
        """Verifies if at least one assigned role is authorized for the target scope."""
        allowed_roles = cls.PERMISSION_ROLES.get(required_permission, [])
        return any(role in allowed_roles for role in assigned_roles)
