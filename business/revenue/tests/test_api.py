import uuid
from datetime import date

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.revenue.api.routes import (
    DecisionGenerateRequest,
    ExplainRequest,
    PredictRequest,
    RecommendationsRequest,
    explain_decision,
    generate_decision,
    get_decision,
    get_forecast,
    get_guest_segment,
    get_kpis,
    get_occupancy,
    get_pricing,
    get_recommendations,
    get_unit_of_work,
    list_decisions,
    list_models,
    predict_cancellation,
)


@pytest.mark.asyncio
async def test_get_unit_of_work() -> None:
    uow = get_unit_of_work()
    assert isinstance(uow, PostgresUnitOfWork)


@pytest.mark.asyncio
async def test_revenue_endpoints_direct(
    db_session: AsyncSession, revenue_setup_data: dict[str, uuid.UUID]
) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore
    category_id = revenue_setup_data["room_category_id"]
    guest_id = revenue_setup_data["guest_id"]
    target_date = date.today()

    # 1. GET /forecast
    fc = await get_forecast(target_date, 30, uow)
    assert len(fc) == 1
    assert fc[0]["target_date"] == target_date.isoformat()

    # Error path for forecast (invalid horizon)
    with pytest.raises(HTTPException) as exc:
        await get_forecast(target_date, 0, uow)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST

    # 2. GET /occupancy
    occ = await get_occupancy(target_date, uow)
    assert occ["target_date"] == target_date

    # 3. GET /pricing
    pr = await get_pricing(category_id, target_date, 0.88, uow)
    assert pr["room_category_id"] == category_id
    assert pr["markup_percentage"] > 0.0

    # Error path for pricing (invalid category id)
    with pytest.raises(HTTPException) as exc:
        await get_pricing(uuid.uuid4(), target_date, 0.88, uow)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    # 4. GET /segments
    seg = await get_guest_segment(guest_id, uow)
    assert seg["guest_id"] == guest_id

    # 5. GET /kpis
    kpis = await get_kpis(uow)
    assert kpis["occupancy_rate"] == 0.745

    # 6. POST /predict
    pred_req = PredictRequest(
        guest_id=guest_id, booking_window=24.0, stay_length=3, spending_history=250.0
    )
    pred = await predict_cancellation(pred_req)
    assert pred["guest_id"] == str(guest_id)
    assert pred["cancellation_probability"] > 0.0

    # 7. POST /recommendations
    rec_req = RecommendationsRequest(
        guest_id=guest_id, current_room_category_id=category_id
    )
    recs = await get_recommendations(rec_req, uow)
    assert recs["guest_id"] == str(guest_id)

    # 8. GET /models
    models = await list_models()
    assert isinstance(models, list)

    # 9. POST /decisions/generate
    gen_req = DecisionGenerateRequest(
        room_category_id=category_id,
        target_date=target_date,
        occupancy_ratio=0.92,
        is_peak_season=True,
    )
    dec_pkg = await generate_decision(gen_req)
    assert dec_pkg["decision_type"] == "PRICING"
    dec_id = uuid.UUID(str(dec_pkg["decision_id"]))

    # 10. GET /decisions
    decs = await list_decisions()
    assert len(decs) >= 1

    # 11. GET /decisions/{id}
    fetched = await get_decision(dec_id)
    assert fetched["decision_id"] == dec_id

    # Error path for get_decision
    with pytest.raises(HTTPException) as exc:
        await get_decision(uuid.uuid4())
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    # 12. POST /decisions/explain
    exp_res = await explain_decision(ExplainRequest(decision_id=dec_id))
    assert exp_res["decision_id"] == str(dec_id)
    assert exp_res["explanation"] is not None

    # Error path for explain_decision
    with pytest.raises(HTTPException) as exc:
        await explain_decision(ExplainRequest(decision_id=uuid.uuid4()))
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
