from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RevenueBaseEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1


class ForecastGenerated(RevenueBaseEvent):
    forecast_id: UUID
    horizon_days: int
    generated_by: str


class OccupancyPredicted(RevenueBaseEvent):
    target_date: datetime
    predicted_occupancy: float
    confidence_lower: float
    confidence_upper: float


class PricingRecommended(RevenueBaseEvent):
    room_category_id: UUID
    target_date: datetime
    recommended_price: float
    base_price: float


class GuestSegmentUpdated(RevenueBaseEvent):
    guest_id: UUID
    old_segment: str | None
    new_segment: str


class ModelRetrained(RevenueBaseEvent):
    model_name: str
    model_version: str
    accuracy_metric: float


class ModelDriftDetected(RevenueBaseEvent):
    model_name: str
    drift_score: float
    metric_name: str


class RecommendationGenerated(RevenueBaseEvent):
    guest_id: UUID
    item_type: str
    score: float


class RevenueAlertCreated(RevenueBaseEvent):
    alert_id: UUID = Field(default_factory=uuid4)
    alert_type: str
    severity: str
    message: str
