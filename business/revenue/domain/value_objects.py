import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class OccupancyForecast(BaseModel):
    target_date: date
    predicted_occupancy: float
    confidence_lower: float
    confidence_upper: float
    room_category_occupancy: dict[str, float] = Field(default_factory=dict)
    vip_occupancy: float = 0.0
    expected_arrivals: int = 0
    expected_departures: int = 0
    room_utilization: float = 0.0


class DemandForecast(BaseModel):
    target_date: date
    booking_demand: float
    walk_in_demand: float
    cancellation_demand: float
    no_show_probability: float
    is_peak_period: bool = False
    is_low_demand: bool = False


class RevenueForecast(BaseModel):
    target_date: date
    predicted_revenue: float
    projected_adr: float
    projected_revpar: float


class CancellationPrediction(BaseModel):
    reservation_id: uuid.UUID
    cancellation_probability: float
    no_show_probability: float


class PricingRecommendation(BaseModel):
    recommendation_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    room_category_id: uuid.UUID
    target_date: date
    recommended_price: float
    base_price: float
    markup_percentage: float
    reason: str
    confidence: float
    loyalty_level_discounts: dict[str, float] = Field(default_factory=dict)


class GuestSegment(BaseModel):
    guest_id: uuid.UUID
    segment_name: str  # Business Traveler, Family, Luxury Traveler, Weekend Traveler, Long Stay, VIP
    stay_frequency: int
    total_spending: float
    loyalty_tier: str
    booking_window_avg: float


class RevenueMetric(BaseModel):
    metric_name: str
    value: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class BusinessKPI(BaseModel):
    occupancy_rate: float
    average_daily_rate: float
    revenue_per_available_room: float
    total_revenue_per_available_room: float
    average_length_of_stay: float
    cancellation_rate: float
    booking_lead_time_avg: float
    revenue_growth_rate: float
    upsell_conversion_rate: float
    cross_sell_conversion_rate: float
    forecast_accuracy_rate: float


class UpsellRecommendation(BaseModel):
    recommendation_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    guest_id: uuid.UUID
    room_category_id: uuid.UUID
    upgrade_price_delta: float
    score: float
    is_accepted: bool = False


class CrossSellRecommendation(BaseModel):
    recommendation_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    guest_id: uuid.UUID
    item_type: str  # Spa, Restaurant, Activity, Package
    item_reference_id: uuid.UUID | None = None
    item_name: str
    price: float
    score: float
    is_accepted: bool = False


class ForecastScenario(BaseModel):
    scenario_name: str  # Optimistic, Pessimistic, Baseline
    multiplier: float
    description: str


class DecisionPackage(BaseModel):
    decision_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    decision_type: (
        str  # PRICING, OCCUPANCY, REVENUE, MARKETING, OPERATIONS, STAFFING, INVENTORY
    )
    prediction: dict[str, Any] = Field(default_factory=dict)
    confidence: float
    recommended_actions: list[str] = Field(default_factory=list)
    expected_business_impact: dict[str, Any] = Field(default_factory=dict)
    reasoning: list[str] = Field(default_factory=list)
    supporting_evidence: list[str] = Field(default_factory=list)
    alternative_options: list[dict[str, Any]] = Field(default_factory=list)
    risk_assessment: dict[str, Any] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
