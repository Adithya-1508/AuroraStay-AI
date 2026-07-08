import uuid
from datetime import date

from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.revenue.domain.exceptions import ForecastingError
from business.revenue.domain.value_objects import PricingRecommendation


class PricingEngine:
    """Computes dynamic markup adjustments and pricing recommendations."""

    def __init__(self) -> None:
        pass

    async def generate_pricing_recommendation(
        self,
        uow: AbstractUnitOfWork,
        room_category_id: uuid.UUID,
        target_date: date,
        occupancy_ratio: float,
        is_peak_season: bool = False,
    ) -> PricingRecommendation:
        """Calculates dynamic markup recommendations without modifying core database prices."""
        async with uow:
            category = await uow.room_categories.get(str(room_category_id))
            if not category:
                raise ForecastingError(
                    f"Room category with ID '{room_category_id}' not found."
                )

            base_price = float(category.base_price)

        # Base markup calculations
        markup_percentage = 0.0
        reason_list = []

        # Occupancy rules
        if occupancy_ratio > 0.85:
            markup_percentage += 0.20
            reason_list.append("High occupancy forecast (>85%)")
        elif occupancy_ratio > 0.70:
            markup_percentage += 0.10
            reason_list.append("Moderate-high occupancy forecast (>70%)")
        elif occupancy_ratio < 0.40:
            markup_percentage -= 0.10
            reason_list.append("Low occupancy forecast (<40%)")

        # Seasonality rules
        if is_peak_season:
            markup_percentage += 0.15
            reason_list.append("Peak demand season curves")

        recommended_price = base_price * (1.0 + markup_percentage)
        reason = ", ".join(reason_list) if reason_list else "Baseline pricing"

        # Standard loyalty level discounts
        loyalty_discounts = {
            "Bronze": 0.0,
            "Silver": 0.05,
            "Gold": 0.10,
            "Platinum": 0.15,
        }

        return PricingRecommendation(
            room_category_id=room_category_id,
            target_date=target_date,
            recommended_price=recommended_price,
            base_price=base_price,
            markup_percentage=markup_percentage,
            reason=reason,
            confidence=0.90,
            loyalty_level_discounts=loyalty_discounts,
        )
