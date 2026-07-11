from typing import Any


class LayoutService:
    """Configures grid positions and widget selections based on user roles."""

    @staticmethod
    def get_layout_for_role(role: str) -> dict[str, Any]:
        normalized_role = role.lower().replace(" ", "_")

        if normalized_role in ["executive", "general_manager"]:
            return {
                "role": role,
                "columns": 12,
                "widgets": [
                    {"widget_id": "widget-health", "col_span": 4, "row_span": 2},
                    {"widget_id": "widget-occupancy", "col_span": 4, "row_span": 2},
                    {
                        "widget_id": "widget-guest-satisfaction",
                        "col_span": 4,
                        "row_span": 2,
                    },
                    {"widget_id": "widget-revenue", "col_span": 8, "row_span": 4},
                    {"widget_id": "widget-alerts", "col_span": 4, "row_span": 4},
                    {"widget_id": "widget-operations", "col_span": 6, "row_span": 2},
                    {"widget_id": "widget-room-status", "col_span": 6, "row_span": 2},
                ],
            }

        elif normalized_role == "revenue_manager":
            return {
                "role": role,
                "columns": 12,
                "widgets": [
                    {"widget_id": "widget-revenue", "col_span": 8, "row_span": 4},
                    {"widget_id": "widget-occupancy", "col_span": 4, "row_span": 2},
                    {"widget_id": "widget-forecast", "col_span": 12, "row_span": 4},
                ],
            }

        elif normalized_role == "operations_manager":
            return {
                "role": role,
                "columns": 12,
                "widgets": [
                    {"widget_id": "widget-operations", "col_span": 6, "row_span": 2},
                    {"widget_id": "widget-room-status", "col_span": 6, "row_span": 2},
                    {"widget_id": "widget-alerts", "col_span": 12, "row_span": 4},
                ],
            }

        else:
            # Fallback/Default Layout (Department Head / Staff)
            return {
                "role": role,
                "columns": 12,
                "widgets": [
                    {"widget_id": "widget-operations", "col_span": 6, "row_span": 2},
                    {"widget_id": "widget-room-status", "col_span": 6, "row_span": 2},
                ],
            }
