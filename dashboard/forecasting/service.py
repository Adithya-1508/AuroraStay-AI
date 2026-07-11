from typing import Any


class DashboardForecastingService:
    """Consolidates forecasting datasets for visualization and scenario comparison."""

    @staticmethod
    def get_forecast_payload(
        horizon_days: int = 30,
        room_type_id: str | None = None,
        compare_historical: bool = True,
    ) -> dict[str, Any]:
        """Formulates forecast packages for charts, including standard comparisons."""
        # Standard mock data generation representing seasonal trends
        data_points = []
        base_occupancy = 0.70
        base_revenue = 12000.00
        base_demand = 75

        for day in range(1, horizon_days + 1):
            # Add simple cyclical weekend demand curves (+10% on Fri/Sat)
            is_weekend = (day % 7) in [5, 6]
            mult = 1.15 if is_weekend else 0.95

            item = {
                "date": f"2026-07-{day:02d}",
                "forecast_occupancy": min(base_occupancy * mult, 1.0),
                "forecast_demand": int(base_demand * mult),
                "forecast_revenue": base_revenue * mult,
            }

            if compare_historical:
                # Historical values (simulated last year / last month)
                hist_mult = mult * 0.96  # 4% growth year-over-year
                item["historical_occupancy"] = min(base_occupancy * hist_mult, 1.0)
                item["historical_revenue"] = base_revenue * hist_mult

            data_points.append(item)

        # Detect any structural anomalies
        anomalies = []
        if horizon_days >= 15:
            anomalies.append(
                {
                    "date": "2026-07-15",
                    "metric": "Demand",
                    "reason": "Unexpected summer festival weekend demand spike (+25%)",
                }
            )

        return {
            "horizon_days": horizon_days,
            "room_type_id": room_type_id,
            "compare_historical": compare_historical,
            "data_points": data_points,
            "anomalies": anomalies,
        }
