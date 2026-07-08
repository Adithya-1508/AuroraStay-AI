import uuid
from datetime import date, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.revenue.application.agent import RevenueAgent
from business.revenue.domain.value_objects import (
    BusinessKPI,
)
from business.revenue.forecasting.service import ForecastingService
from business.revenue.ml.registry import ModelRegistry
from business.revenue.pricing.engine import PricingEngine
from business.revenue.recommendations.service import RecommendationService
from business.revenue.segmentation.clusterer import GuestSegmenter

router = APIRouter(prefix="/revenue", tags=["Revenue"])

# Shared services instances
forecasting_service = ForecastingService()
pricing_engine = PricingEngine()
rec_service = RecommendationService()
segmenter = GuestSegmenter()
model_registry = ModelRegistry()
revenue_agent = RevenueAgent(forecasting_service, pricing_engine)

# In-memory storage for decisions
decisions_cache: dict[uuid.UUID, dict[str, Any]] = {}


def get_unit_of_work() -> PostgresUnitOfWork:
    """Dependency injector resolving concrete PostgresUnitOfWork transactions."""
    return PostgresUnitOfWork()


# 1. Forecasting & Occupancy
@router.get("/forecast", response_model=list[dict[str, Any]])
async def get_forecast(
    target_date: date,
    horizon_days: int = 30,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> list[dict[str, Any]]:
    try:
        occupancy = await forecasting_service.generate_occupancy_forecast(
            uow, target_date, horizon_days
        )
        revenue = await forecasting_service.generate_revenue_forecast(
            uow, target_date, occupancy.predicted_occupancy
        )
        demand = await forecasting_service.generate_demand_forecast(uow, target_date)
        return [
            {
                "target_date": target_date.isoformat(),
                "occupancy": occupancy.model_dump(),
                "revenue": revenue.model_dump(),
                "demand": demand.model_dump(),
            }
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Forecasting calculation failed: {str(e)}",
        ) from e


@router.get("/occupancy", response_model=dict[str, Any])
async def get_occupancy(
    target_date: date, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    res = await forecasting_service.generate_occupancy_forecast(uow, target_date, 30)
    return res.model_dump()


# 2. Dynamic Pricing Recommendations
@router.get("/pricing", response_model=dict[str, Any])
async def get_pricing(
    room_category_id: uuid.UUID,
    target_date: date,
    occupancy_ratio: float = 0.75,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    try:
        res = await pricing_engine.generate_pricing_recommendation(
            uow, room_category_id, target_date, occupancy_ratio
        )
        return res.model_dump()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


# 3. Guest Segmentation
@router.get("/segments", response_model=dict[str, Any])
async def get_guest_segment(
    guest_id: uuid.UUID, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    res = await segmenter.segment_guest(uow, guest_id)
    return res.model_dump()


# 4. Business KPIs
@router.get("/kpis", response_model=dict[str, Any])
async def get_kpis(
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    # Compute mock KPIs representing system averages
    kpi = BusinessKPI(
        occupancy_rate=0.745,
        average_daily_rate=124.50,
        revenue_per_available_room=92.75,
        total_revenue_per_available_room=115.40,
        average_length_of_stay=3.2,
        cancellation_rate=0.12,
        booking_lead_time_avg=18.5,
        revenue_growth_rate=0.084,
        upsell_conversion_rate=0.15,
        cross_sell_conversion_rate=0.22,
        forecast_accuracy_rate=0.915,
    )
    return kpi.model_dump()


# 5. Predictions & ML Inference Endpoints
class PredictRequest(BaseModel):
    guest_id: uuid.UUID
    booking_window: float
    stay_length: int
    spending_history: float


@router.post("/predict", response_model=dict[str, Any])
async def predict_cancellation(req: PredictRequest) -> dict[str, Any]:
    # Mock cancellation prediction based on stay length & lead window
    prob = min(0.95, max(0.01, (req.booking_window / 100.0) + (req.stay_length * 0.05)))
    return {
        "guest_id": str(req.guest_id),
        "cancellation_probability": prob,
        "no_show_probability": prob * 0.2,
    }


class RecommendationsRequest(BaseModel):
    guest_id: uuid.UUID
    current_room_category_id: uuid.UUID | None = None


@router.post("/recommendations", response_model=dict[str, Any])
async def get_recommendations(
    req: RecommendationsRequest, uow: PostgresUnitOfWork = Depends(get_unit_of_work)
) -> dict[str, Any]:
    upsell = None
    if req.current_room_category_id:
        upsell_res = await rec_service.generate_upsell_recommendation(
            uow, req.guest_id, req.current_room_category_id
        )
        if upsell_res:
            upsell = upsell_res.model_dump()

    cross = await rec_service.generate_cross_sell_recommendations(uow, req.guest_id)
    return {
        "guest_id": str(req.guest_id),
        "upsell": upsell,
        "cross_sell": [c.model_dump() for c in cross],
    }


# 6. Model Registry Listing
@router.get("/models", response_model=list[dict[str, Any]])
async def list_models() -> list[dict[str, Any]]:
    models = model_registry.list_models()
    return [m.model_dump() for m in models]


# 7. Decision Intelligence APIs
@router.get("/decisions", response_model=list[dict[str, Any]])
async def list_decisions() -> list[dict[str, Any]]:
    return list(decisions_cache.values())


class DecisionGenerateRequest(BaseModel):
    room_category_id: uuid.UUID
    target_date: date
    occupancy_ratio: float = 0.88
    is_peak_season: bool = False


@router.post("/decisions/generate", response_model=dict[str, Any])
async def generate_decision(req: DecisionGenerateRequest) -> dict[str, Any]:
    target_dt = datetime(
        req.target_date.year, req.target_date.month, req.target_date.day
    )
    res = await revenue_agent.run_workflow(
        req.room_category_id, target_dt, req.occupancy_ratio, req.is_peak_season
    )
    # Save package in cache
    pkg = res["decision_package"]
    dec_id = uuid.UUID(str(pkg["decision_id"]))
    decisions_cache[dec_id] = {"decision": pkg, "explanation": res["explanation"]}
    return pkg  # type: ignore[no-any-return]


@router.get("/decisions/{id}", response_model=dict[str, Any])
async def get_decision(id: uuid.UUID) -> dict[str, Any]:
    if id not in decisions_cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Decision package with ID '{id}' not found.",
        )
    return decisions_cache[id]["decision"]  # type: ignore[no-any-return]


class ExplainRequest(BaseModel):
    decision_id: uuid.UUID


@router.post("/decisions/explain", response_model=dict[str, Any])
async def explain_decision(req: ExplainRequest) -> dict[str, Any]:
    if req.decision_id not in decisions_cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Decision package with ID '{req.decision_id}' not found.",
        )
    return {
        "decision_id": str(req.decision_id),
        "explanation": decisions_cache[req.decision_id]["explanation"],
    }
