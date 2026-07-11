from backend.auth.permissions import require_role

# Roles allowed for overall executive access
EXECUTIVE_ROLES = ["Executive", "General Manager"]

# Roles allowed for revenue features
REVENUE_ROLES = ["Executive", "General Manager", "Revenue Manager"]

# Roles allowed for operations features
OPERATIONS_ROLES = ["Executive", "General Manager", "Operations Manager"]

# Roles allowed for guest features
GUEST_ROLES = [
    "Executive",
    "General Manager",
    "Guest Experience Manager",
    "Operations Manager",
]

# Dependency-injected guards
require_executive = require_role(EXECUTIVE_ROLES)
require_revenue = require_role(REVENUE_ROLES)
require_operations = require_role(OPERATIONS_ROLES)
require_guest = require_role(GUEST_ROLES)

__all__ = [
    "EXECUTIVE_ROLES",
    "REVENUE_ROLES",
    "OPERATIONS_ROLES",
    "GUEST_ROLES",
    "require_executive",
    "require_revenue",
    "require_operations",
    "require_guest",
]
