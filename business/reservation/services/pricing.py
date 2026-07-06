from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.reservation.domain.exceptions import InventoryExhaustedError
from business.reservation.domain.value_objects import BookingWindow
from business.reservation.pricing.engine import CostBreakdown, PricingEngine


class PricingService:
    """Application Service calculating reservation stay costs."""

    def __init__(self, engine: PricingEngine | None = None) -> None:
        self.engine = engine or PricingEngine()

    async def calculate_reservation_price(
        self,
        uow: AbstractUnitOfWork,
        room_category_id: str,
        window: BookingWindow,
        loyalty_tier: str = "Bronze",
        promo_code: str | None = None,
    ) -> CostBreakdown:
        """Loads room category base rate and invokes pricing engine."""
        # 1. Fetch category base price
        category = await uow.room_categories.get(str(room_category_id))
        if not category:
            raise InventoryExhaustedError(
                f"Room Category '{room_category_id}' not found."
            )

        # 2. Calculate price using pricing engine
        return self.engine.calculate_price(
            base_nightly_price=category.base_price,
            check_in_date=window.check_in_date,
            check_out_date=window.check_out_date,
            loyalty_tier=loyalty_tier,
            promo_code=promo_code,
        )


__all__ = ["PricingService"]
