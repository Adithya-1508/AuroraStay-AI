# Core enterprise role list
ENTERPRISE_ROLES = [
    "Guest",
    "Receptionist",
    "Housekeeping",
    "Maintenance",
    "Restaurant",
    "Spa",
    "Revenue Manager",
    "Operations Manager",
    "General Manager",
    "Administrator",
    "System Administrator",
    "AI Administrator",
    "ML Engineer",
    "Developer",
    "Auditor",
    "Service Account",
]

# Role to direct permissions mapping
ROLE_PERMISSIONS: dict[str, list[str]] = {
    "Guest": ["reservation:read"],
    "Receptionist": ["reservation:read", "reservation:write"],
    "Housekeeping": ["housekeeping:read", "housekeeping:write"],
    "Revenue Manager": ["revenue:read", "revenue:write"],
    "Operations Manager": [
        "reservation:read",
        "reservation:write",
        "housekeeping:read",
        "revenue:read",
    ],
    "General Manager": [
        "reservation:read",
        "reservation:write",
        "housekeeping:read",
        "revenue:read",
    ],
    "Administrator": [
        "reservation:read",
        "reservation:write",
        "housekeeping:read",
        "housekeeping:write",
        "revenue:read",
        "revenue:write",
    ],
    "System Administrator": ["audit:read", "model:approve"],
    "AI Administrator": ["model:approve"],
    "ML Engineer": ["model:approve"],
    "Auditor": ["audit:read"],
}


class RBACManager:
    """Manages role hierarchical inheritance and permissions queries."""

    @staticmethod
    def get_permissions_for_roles(roles: list[str]) -> list[str]:
        """Collects deduplicated permission strings across a list of roles."""
        perms = set()
        for role in roles:
            if role in ROLE_PERMISSIONS:
                perms.update(ROLE_PERMISSIONS[role])
        return list(perms)
