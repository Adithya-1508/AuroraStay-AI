from backend.repositories.base import AbstractRepository
from backend.repositories.forecast import AbstractForecastRepository
from backend.repositories.guest import AbstractGuestRepository
from backend.repositories.housekeeping import AbstractHousekeepingRepository
from backend.repositories.knowledge import AbstractKnowledgeRepository
from backend.repositories.maintenance import AbstractMaintenanceRepository
from backend.repositories.postgres.forecast import ForecastRepository
from backend.repositories.postgres.guest import GuestRepository
from backend.repositories.postgres.housekeeping import HousekeepingRepository
from backend.repositories.postgres.knowledge import KnowledgeRepository
from backend.repositories.postgres.maintenance import MaintenanceRepository
from backend.repositories.postgres.recommendation import RecommendationRepository
from backend.repositories.postgres.reservation import ReservationRepository
from backend.repositories.postgres.review import ReviewRepository
from backend.repositories.recommendation import AbstractRecommendationRepository
from backend.repositories.reservation import AbstractReservationRepository
from backend.repositories.review import AbstractReviewRepository

__all__ = [
    "AbstractRepository",
    "AbstractGuestRepository",
    "AbstractReservationRepository",
    "AbstractReviewRepository",
    "AbstractKnowledgeRepository",
    "AbstractForecastRepository",
    "AbstractRecommendationRepository",
    "AbstractHousekeepingRepository",
    "AbstractMaintenanceRepository",
    "GuestRepository",
    "ReservationRepository",
    "ReviewRepository",
    "KnowledgeRepository",
    "ForecastRepository",
    "RecommendationRepository",
    "HousekeepingRepository",
    "MaintenanceRepository",
]
