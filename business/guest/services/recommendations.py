import uuid
from datetime import datetime

from backend.models.recommendation import Recommendation
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.guest.domain.exceptions import GuestNotFoundError
from business.guest.events.publisher import domain_event_publisher
from business.guest.events.schemas import RecommendationGenerated


class RecommendationEngine:
    """Service to dynamically generate personalized upsells and facility recommendations."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def generate_recommendations(
        self, guest_id: uuid.UUID
    ) -> list[Recommendation]:
        """Generates dynamic restaurant, spa, and upgrade recommendations for a guest."""
        async with self.uow:
            guest = await self.uow.guests.get(str(guest_id))
            if not guest:
                raise GuestNotFoundError(str(guest_id))

            prefs = guest.preferences or {}
            dietary = prefs.get("dietary_restrictions", [])
            tier = guest.loyalty_tier or "Bronze"

            recommendations = []

            # 1. Room Upgrade Offer (Loyalty-Based)
            if tier in ["Platinum", "VIP"]:
                upgrade_rec = Recommendation(
                    guest_id=guest_id,
                    item_type="Room Upgrade",
                    item_reference_id=None,
                    score=0.99,
                    is_accepted=False,
                    generated_at=datetime.utcnow(),
                )
                recommendations.append(upgrade_rec)

            # 2. Restaurant Suggestion (Dietary-Based)
            if "Vegetarian" in dietary or "Vegan" in dietary:
                dining_rec = Recommendation(
                    guest_id=guest_id,
                    item_type="Vegetarian Dining at Aurora Bistro",
                    item_reference_id=None,
                    score=0.95,
                    is_accepted=False,
                    generated_at=datetime.utcnow(),
                )
                recommendations.append(dining_rec)

            # 3. Spa Suggestion (Default high-tier fallback)
            spa_rec = Recommendation(
                guest_id=guest_id,
                item_type="Zen Premium Spa Therapy",
                item_reference_id=None,
                score=0.85,
                is_accepted=False,
                generated_at=datetime.utcnow(),
            )
            recommendations.append(spa_rec)

            # Save generated recommendations to database
            for rec in recommendations:
                await self.uow.recommendations.add(rec)

            await self.uow.commit()

            # Publish events
            for rec in recommendations:
                await domain_event_publisher.publish(
                    RecommendationGenerated(
                        recommendation_id=rec.id,
                        guest_id=rec.guest_id,
                        item_type=rec.item_type,
                        score=float(rec.score),
                    )
                )

            return recommendations

    async def get_guest_recommendations(
        self, guest_id: uuid.UUID
    ) -> list[Recommendation]:
        """Retrieves previously generated recommendations for a guest."""
        async with self.uow:
            guest = await self.uow.guests.get(str(guest_id))
            if not guest:
                raise GuestNotFoundError(str(guest_id))

            recs = await self.uow.recommendations.get_all()
            return [r for r in recs if r.guest_id == guest_id]
