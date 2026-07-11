from typing import Any


class AnalyticsService:
    """Handles drill-down queries for revenue, operations, and guest platforms."""

    @staticmethod
    def get_sliced_analytics(
        department: str | None = None,
        room_type: str | None = None,
        guest_segment: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        revenue_source: str | None = None,
    ) -> dict[str, Any]:
        """Filters and slices aggregated hospitality metrics."""
        # Baseline/Default simulated aggregates
        raw_revenue = 145000.00
        raw_bookings = 350
        raw_tasks = 480
        sla_compliance = 0.94
        avg_satisfaction = 4.6

        # Apply mock adjustments based on filters for dynamic responses
        if department:
            if department.lower() == "housekeeping":
                raw_tasks = 320
                sla_compliance = 0.96
            elif department.lower() == "maintenance":
                raw_tasks = 160
                sla_compliance = 0.90

        if room_type:
            if "suite" in room_type.lower():
                raw_revenue = 92000.00
                raw_bookings = 120
            else:
                raw_revenue = 53000.00
                raw_bookings = 230

        if guest_segment:
            if guest_segment.lower() == "corporate":
                raw_bookings = 150
                avg_satisfaction = 4.4
            elif guest_segment.lower() == "leisure":
                raw_bookings = 200
                avg_satisfaction = 4.8

        if revenue_source:
            if revenue_source.lower() == "spa":
                raw_revenue = 18500.00
            elif revenue_source.lower() == "restaurant":
                raw_revenue = 34000.00
            elif revenue_source.lower() == "room":
                raw_revenue = 92500.00

        return {
            "filters_applied": {
                "department": department,
                "room_type": room_type,
                "guest_segment": guest_segment,
                "start_date": start_date,
                "end_date": end_date,
                "revenue_source": revenue_source,
            },
            "kpis": {
                "revenue": raw_revenue,
                "adr": raw_revenue / max(raw_bookings, 1),
                "bookings_count": raw_bookings,
                "operational_tasks": raw_tasks,
                "sla_compliance_rate": sla_compliance,
                "guest_satisfaction_rating": avg_satisfaction,
            },
            "breakdowns": {
                "by_room_type": [
                    {"room_type": "Deluxe Suite", "revenue": raw_revenue * 0.6},
                    {"room_type": "Standard Queen", "revenue": raw_revenue * 0.4},
                ],
                "by_guest_segment": [
                    {"segment": "Leisure", "bookings": int(raw_bookings * 0.57)},
                    {"segment": "Corporate", "bookings": int(raw_bookings * 0.43)},
                ],
                "by_revenue_source": [
                    {"source": "Room Charges", "amount": raw_revenue * 0.65},
                    {"source": "Food & Beverage", "amount": raw_revenue * 0.23},
                    {"source": "Spa & Ancillary", "amount": raw_revenue * 0.12},
                ],
            },
        }
