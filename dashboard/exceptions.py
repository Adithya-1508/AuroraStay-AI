class DashboardError(Exception):
    """Base exception for dashboard operations."""

    pass


class RolePermissionError(DashboardError):
    """Raised when a user lacks the necessary role for a dashboard view."""

    pass


class ReportGenerationError(DashboardError):
    """Raised when report compilation or export fails."""

    pass


class AssistantError(DashboardError):
    """Raised when the AI Executive Assistant fails to execute the reasoning graph."""

    pass
