import uuid
from datetime import date, datetime
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.revenue.application.agent import RevenueAgent
from business.revenue.domain.exceptions import ForecastingError
from business.revenue.forecasting.service import ForecastingService
from business.revenue.ml.registry import ModelRegistration, ModelRegistry
from business.revenue.ml.tracker import MLflowTracker
from business.revenue.pipelines.monitoring import MonitoringPipeline
from business.revenue.pipelines.training import TrainingPipeline
from business.revenue.pricing.engine import PricingEngine
from business.revenue.recommendations.service import RecommendationService
from business.revenue.segmentation.clusterer import GuestSegmenter


@pytest.mark.asyncio
async def test_forecasting_and_pricing_services(
    db_session: AsyncSession, revenue_setup_data: dict[str, uuid.UUID]
) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    category_id = revenue_setup_data["room_category_id"]

    forecaster = ForecastingService()
    pricing = PricingEngine()

    # 1. Occupancy Forecast
    target_date = date.today()
    fc = await forecaster.generate_occupancy_forecast(uow, target_date, 30)
    assert fc.target_date == target_date
    assert fc.predicted_occupancy == 0.65  # Baseline fallback
    assert fc.confidence_lower == pytest.approx(0.60)
    assert fc.confidence_upper == pytest.approx(0.70)

    # Test error bounds
    with pytest.raises(ForecastingError):
        await forecaster.generate_occupancy_forecast(uow, target_date, 0)

    # 2. Demand Forecast
    df = await forecaster.generate_demand_forecast(uow, target_date)
    assert df.target_date == target_date
    assert df.booking_demand > 0
    assert df.cancellation_demand > 0

    # 3. Revenue Forecast
    rf = await forecaster.generate_revenue_forecast(
        uow, target_date, fc.predicted_occupancy
    )
    assert rf.predicted_revenue > 0

    # 4. Pricing Recommendation
    rec = await pricing.generate_pricing_recommendation(
        uow, category_id, target_date, fc.predicted_occupancy
    )
    assert rec.room_category_id == category_id
    assert rec.base_price == 200.0
    assert rec.markup_percentage == 0.0  # Moderate baseline

    # Pricing error path
    with pytest.raises(ForecastingError):
        await pricing.generate_pricing_recommendation(
            uow, uuid.uuid4(), target_date, 0.5
        )


@pytest.mark.asyncio
async def test_guest_segmentation(
    db_session: AsyncSession, revenue_setup_data: dict[str, uuid.UUID]
) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    guest_id = revenue_setup_data["guest_id"]

    segmenter = GuestSegmenter()

    # Segment existing guest
    seg = await segmenter.segment_guest(uow, guest_id)
    assert seg.guest_id == guest_id
    assert seg.segment_name == "VIP"  # Gold loyalty tier rule
    assert seg.total_spending == 0.0

    # Segment non-existent guest (fallback check)
    fallback_seg = await segmenter.segment_guest(uow, uuid.uuid4())
    assert fallback_seg.segment_name == "Weekend Traveler"

    # Train segmentation
    train_res = await segmenter.train_segmentation(
        [{"stay_frequency": 5, "total_spending": 800.0}]
    )
    assert "inertia" in train_res


@pytest.mark.asyncio
async def test_recommendations(
    db_session: AsyncSession, revenue_setup_data: dict[str, uuid.UUID]
) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    guest_id = revenue_setup_data["guest_id"]
    category_id = revenue_setup_data["room_category_id"]
    cheaper_id = revenue_setup_data["cheaper_category_id"]

    service = RecommendationService()

    # Generate upsell upgrade (should be None since category_id is the most expensive suite)
    upsell = await service.generate_upsell_recommendation(uow, guest_id, category_id)
    assert upsell is None

    # Generate upsell upgrade from cheaper category (should succeed and upsell to the Revenue Suite)
    upsell_success = await service.generate_upsell_recommendation(
        uow, guest_id, cheaper_id
    )
    assert upsell_success is not None
    assert upsell_success.room_category_id == category_id
    assert upsell_success.upgrade_price_delta == 100.0

    # Try non-existent category
    null_upsell = await service.generate_upsell_recommendation(
        uow, guest_id, uuid.uuid4()
    )
    assert null_upsell is None

    # Generate cross-sell offers
    cross = await service.generate_cross_sell_recommendations(uow, guest_id)
    assert len(cross) == 2
    assert cross[0].item_type == "Spa"
    assert cross[1].item_type == "Restaurant"


@pytest.mark.asyncio
async def test_ml_pipelines_and_monitoring() -> None:
    registry = ModelRegistry()
    tracker = MLflowTracker()
    training = TrainingPipeline(registry, tracker)
    monitoring = MonitoringPipeline(registry, tracker)

    # 1. Train forecasting model
    m1 = await training.run_forecasting_training()
    assert m1.model_name == "OccupancyRegressor"
    assert m1.deployment_status == "Production"

    # 2. Train segmentation model
    m2 = await training.run_segmentation_training()
    assert m2.model_name == "GuestClusterer"

    # 3. Model registry checks
    assert registry.get_model(m1.model_id) == m1
    assert len(registry.list_models()) == 2
    assert registry.get_latest_production("OccupancyRegressor") == m1

    # Promotion check
    registry.promote_to_production(m2.model_id)
    assert m2.deployment_status == "Production"

    # Rollback check
    rollback_res = registry.rollback("OccupancyRegressor")
    assert rollback_res is None  # only 1 version exists

    # Add second model version for rollback
    m1_v2 = ModelRegistration(
        model_name="OccupancyRegressor",
        version="1.1.0",
        training_dataset="hospital_bookings_2025_v2",
        metrics={"R2_score": 0.92},
        owner="Revenue ML Team",
        deployment_status="Production",
    )
    registry.register_model(m1_v2)
    registry.promote_to_production(m1_v2.model_id)

    rolled = registry.rollback("OccupancyRegressor")
    assert rolled is not None
    assert rolled.version == "1.0.0"

    # 4. Drift monitoring
    drift = await monitoring.check_drift(
        "OccupancyRegressor", [0.8, 0.9, 0.75], [0.5, 0.45, 0.55]
    )
    assert drift["drift_detected"] is True
    assert drift["drift_score"] > 0.15

    # Edge cases for drift checks
    empty_drift = await monitoring.check_drift("OccupancyRegressor", [], [])
    assert empty_drift["drift_detected"] is False

    await monitoring.log_inference_metrics(12.4, False)


@pytest.mark.asyncio
async def test_revenue_agent() -> None:
    forecaster = ForecastingService()
    pricing = PricingEngine()
    agent = RevenueAgent(forecaster, pricing)

    category_id = uuid.uuid4()
    target_dt = datetime.utcnow()

    res = await agent.run_workflow(category_id, target_dt, 0.92, True)
    assert res["policy_docs"] == "Standard pricing policy limits markups to 30%."
    assert (
        "Adjust dynamic pricing rate markup to 30%"
        in res["decision_package"]["recommended_actions"][0]
    )
    assert res["explanation"] is not None


@pytest.mark.asyncio
async def test_pricing_engine_occupancy_branches(
    db_session: AsyncSession, revenue_setup_data: dict[str, uuid.UUID]
) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    category_id = revenue_setup_data["room_category_id"]
    pricing = PricingEngine()
    target_date = date.today()

    # Moderate occupancy ratio (0.75)
    rec1 = await pricing.generate_pricing_recommendation(
        uow, category_id, target_date, 0.75
    )
    assert rec1.markup_percentage == pytest.approx(0.10)
    assert "Moderate-high occupancy forecast (>70%)" in rec1.reason

    # Low occupancy ratio (0.30)
    rec2 = await pricing.generate_pricing_recommendation(
        uow, category_id, target_date, 0.30
    )
    assert rec2.markup_percentage == pytest.approx(-0.10)
    assert "Low occupancy forecast (<40%)" in rec2.reason

    # Peak season with high occupancy ratio (0.90)
    rec3 = await pricing.generate_pricing_recommendation(
        uow, category_id, target_date, 0.90, is_peak_season=True
    )
    assert rec3.markup_percentage == pytest.approx(0.35)
    assert "High occupancy forecast (>85%)" in rec3.reason
    assert "Peak demand season curves" in rec3.reason


@pytest.mark.asyncio
async def test_guest_segmentation_rules(
    db_session: AsyncSession, revenue_setup_data: dict[str, uuid.UUID]
) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    guest_id = revenue_setup_data["guest_id"]
    category_id = revenue_setup_data["room_category_id"]
    segmenter = GuestSegmenter()

    # Train segmentation with >= 4 guests to fit KMeans
    train_res = await segmenter.train_segmentation(
        [
            {"stay_frequency": 2, "total_spending": 200.0},
            {"stay_frequency": 5, "total_spending": 800.0},
            {"stay_frequency": 1, "total_spending": 100.0},
            {"stay_frequency": 10, "total_spending": 2000.0},
        ]
    )
    assert "inertia" in train_res

    # Test rule: loyalty_tier Gold/Platinum -> VIP
    seg_vip = await segmenter.segment_guest(uow, guest_id)
    assert seg_vip.segment_name == "VIP"

    # Modify guest loyalty tier & check rule-based segments
    async with uow:
        guest = await uow.guests.get(str(guest_id))
        assert guest is not None
        guest.loyalty_tier = "Bronze"
        await uow.commit()

    # Test rule: stay_count >= 5 -> Business Traveler
    # Create mock reservations for the guest
    from backend.models.reservation import Reservation

    async with uow:
        for _ in range(5):
            res = Reservation(
                guest_id=guest_id,
                room_category_id=category_id,
                check_in_date=date.today(),
                check_out_date=date.today(),
                total_cost=200.0,
                status="Confirmed",
            )
            uow.session.add(res)
        await uow.commit()

    seg_bus = await segmenter.segment_guest(uow, guest_id)
    assert seg_bus.segment_name == "Business Traveler"
    assert seg_bus.total_spending == 1000.0

    # Test rule: total_spent > 1500.0 -> Luxury Traveler
    async with uow:
        res = Reservation(
            guest_id=guest_id,
            room_category_id=category_id,
            check_in_date=date.today(),
            check_out_date=date.today(),
            total_cost=1000.0,
            status="Confirmed",
        )
        uow.session.add(res)
        await uow.commit()

    seg_lux = await segmenter.segment_guest(uow, guest_id)
    assert seg_lux.segment_name == "Luxury Traveler"

    # Test rule: total_spent > 500.0 and stay_count >= 2 -> Long Stay
    # Reset reservation state
    async with uow:
        from sqlalchemy import delete

        await uow.session.execute(
            delete(Reservation).where(Reservation.guest_id == guest_id)
        )
        # Add 2 reservations totaling 600
        r1 = Reservation(
            guest_id=guest_id,
            room_category_id=category_id,
            check_in_date=date.today(),
            check_out_date=date.today(),
            total_cost=300.0,
            status="Confirmed",
        )
        r2 = Reservation(
            guest_id=guest_id,
            room_category_id=category_id,
            check_in_date=date.today(),
            check_out_date=date.today(),
            total_cost=300.0,
            status="Confirmed",
        )
        uow.session.add(r1)
        uow.session.add(r2)
        await uow.commit()

    seg_long = await segmenter.segment_guest(uow, guest_id)
    assert seg_long.segment_name == "Long Stay"


@pytest.mark.asyncio
async def test_ml_tracker_mock_mlflow(monkeypatch: pytest.MonkeyPatch) -> None:
    # Force MLflow available to cover standard MLflow tracking pathways
    import sys
    from types import ModuleType

    mock_mlflow: Any = ModuleType("mlflow")
    mock_mlflow.set_tracking_uri = lambda uri: None
    mock_mlflow.set_experiment = lambda exp: None
    mock_mlflow.start_run = lambda run_name=None: "real_mlflow_run"
    mock_mlflow.end_run = lambda: None
    mock_mlflow.log_param = lambda k, v: None
    mock_mlflow.log_metric = lambda k, v: None
    mock_mlflow.sklearn = ModuleType("sklearn")
    mock_mlflow.sklearn.log_model = lambda m, p: None

    sys.modules["mlflow"] = mock_mlflow

    # Reload tracker or patch MLFLOW_AVAILABLE
    import business.revenue.ml.tracker as tracker_mod

    monkeypatch.setattr(tracker_mod, "MLFLOW_AVAILABLE", True)
    monkeypatch.setattr(tracker_mod, "mlflow", mock_mlflow)

    tracker = tracker_mod.MLflowTracker()
    assert tracker.start_run("TestExp") == "real_mlflow_run"
    tracker.log_param("test_param", 12)
    tracker.log_metric("test_metric", 0.95)
    tracker.log_model(None, "model_path")
    tracker.end_run()


@pytest.mark.asyncio
async def test_revenue_agent_low_occupancy_and_rag() -> None:
    # 1. Low occupancy agent workflow
    forecaster = ForecastingService()
    pricing = PricingEngine()
    agent = RevenueAgent(forecaster, pricing)

    category_id = uuid.uuid4()
    target_dt = datetime.utcnow()
    res = await agent.run_workflow(category_id, target_dt, 0.35, False)
    assert (
        "Adjust dynamic pricing rate markup to -10%"
        in res["decision_package"]["recommended_actions"][0]
    )

    # 2. Mock RAG retriever
    class MockRetriever:
        async def retrieve(self, query: str) -> list[Any]:
            class Doc:
                content = "Under peak seasons, markups are capped at 30%."

            return [Doc()]

    agent_rag = RevenueAgent(forecaster, pricing, retriever=MockRetriever())
    res_rag = await agent_rag.run_workflow(category_id, target_dt, 0.95, True)
    assert (
        "capp" in res_rag["explanation"].lower()
        or "markup" in res_rag["explanation"].lower()
    )


def test_events_schemas_instantiation() -> None:
    from business.revenue.events.schemas import (
        ForecastGenerated,
        GuestSegmentUpdated,
        ModelDriftDetected,
        ModelRetrained,
        OccupancyPredicted,
        PricingRecommended,
        RecommendationGenerated,
        RevenueAlertCreated,
    )

    # Simple instantiation of all event schemas to ensure they validate and register coverage
    g_id = uuid.uuid4()
    c_id = uuid.uuid4()
    dt = datetime.now()

    e1 = ForecastGenerated(
        forecast_id=uuid.uuid4(), horizon_days=30, generated_by="API"
    )
    assert e1.horizon_days == 30

    e2 = OccupancyPredicted(
        target_date=dt,
        predicted_occupancy=0.85,
        confidence_lower=0.80,
        confidence_upper=0.90,
    )
    assert e2.predicted_occupancy == 0.85

    e3 = PricingRecommended(
        room_category_id=c_id, target_date=dt, recommended_price=250.0, base_price=200.0
    )
    assert e3.recommended_price == 250.0

    e4 = GuestSegmentUpdated(guest_id=g_id, old_segment="Bronze", new_segment="Silver")
    assert e4.new_segment == "Silver"

    e5 = ModelRetrained(
        model_name="OccupancyRegressor", model_version="1.0.0", accuracy_metric=0.89
    )
    assert e5.model_version == "1.0.0"

    e6 = ModelDriftDetected(
        model_name="OccupancyRegressor", drift_score=0.25, metric_name="MSE"
    )
    assert e6.drift_score == 0.25

    e7 = RecommendationGenerated(guest_id=g_id, item_type="SpaOffer", score=0.88)
    assert e7.score == 0.88

    e8 = RevenueAlertCreated(
        alert_type="Drift", severity="High", message="Drift detected"
    )
    assert e8.severity == "High"
