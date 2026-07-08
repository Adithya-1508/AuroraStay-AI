import uuid
from datetime import datetime

from backend.models.recommendation import Recommendation as DBRecommendation
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.revenue.domain.value_objects import (
    CrossSellRecommendation,
    UpsellRecommendation,
)


class RecommendationService:
    """Calculates, saves, and ranks personalized upsell and cross-sell recommendations."""

    def __init__(self) -> None:
        pass

    async def generate_upsell_recommendation(
        self,
        uow: AbstractUnitOfWork,
        guest_id: uuid.UUID,
        current_category_id: uuid.UUID,
    ) -> UpsellRecommendation | None:
        """Finds next-tier room categories to suggest as upsell upgrades."""
        async with uow:
            # Query all category prices
            cats = await uow.room_categories.get_all()
            current = await uow.room_categories.get(str(current_category_id))
            if not current:
                return None

            # Filter upgrade categories
            upgrades = [
                c for c in cats if float(c.base_price) > float(current.base_price)
            ]
            if not upgrades:
                return None

            # Pick the next-cheapest upgrade category
            target_upgrade = min(upgrades, key=lambda x: float(x.base_price))
            delta = float(target_upgrade.base_price) - float(current.base_price)

            # Persist generic recommendation to database
            db_rec = DBRecommendation(
                guest_id=guest_id,
                item_type="RoomUpgrade",
                item_reference_id=target_upgrade.id,
                score=0.85,
                is_accepted=False,
                generated_at=datetime.utcnow(),
            )
            await uow.recommendations.add(db_rec)
            await uow.commit()

            return UpsellRecommendation(
                recommendation_id=db_rec.id,
                guest_id=guest_id,
                room_category_id=target_upgrade.id,
                upgrade_price_delta=delta,
                score=0.85,
            )

    async def generate_cross_sell_recommendations(
        self, uow: AbstractUnitOfWork, guest_id: uuid.UUID
    ) -> list[CrossSellRecommendation]:
        """Generates cross-sells for Spa, Restaurant, and Packages."""
        async with uow:
            # Check if any spas exist
            spas = await uow.spas.get_all() if hasattr(uow, "spas") else []
            spa_ref_id = spas[0].id if spas else None

        cross_sells = []

        # 1. Spa offer
        db_spa = DBRecommendation(
            guest_id=guest_id,
            item_type="SpaOffer",
            item_reference_id=spa_ref_id,
            score=0.75,
            is_accepted=False,
            generated_at=datetime.utcnow(),
        )
        # 2. Restaurant offer
        db_rest = DBRecommendation(
            guest_id=guest_id,
            item_type="RestaurantOffer",
            item_reference_id=None,
            score=0.80,
            is_accepted=False,
            generated_at=datetime.utcnow(),
        )

        async with uow:
            await uow.recommendations.add(db_spa)
            await uow.recommendations.add(db_rest)
            await uow.commit()

        cross_sells.append(
            CrossSellRecommendation(
                recommendation_id=db_spa.id,
                guest_id=guest_id,
                item_type="Spa",
                item_reference_id=spa_ref_id,
                item_name="Swedish Massage Discount",
                price=80.0,
                score=0.75,
            )
        )
        cross_sells.append(
            CrossSellRecommendation(
                recommendation_id=db_rest.id,
                guest_id=guest_id,
                item_type="Restaurant",
                item_reference_id=None,
                item_name="Fine Dining Wine Pairing",
                price=45.0,
                score=0.80,
            )
        )
        return cross_sells
