from datetime import date, timedelta

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.guest import Guest
from backend.models.room import Room, RoomCategory
from business.reservation.api.routes import router as reservations_router


@pytest.fixture
def test_app(db_session: AsyncSession) -> FastAPI:
    """Creates a test FastAPI application with overridden database session."""
    app = FastAPI()
    app.include_router(reservations_router)

    from backend.repositories.unit_of_work import PostgresUnitOfWork
    from business.reservation.api.routes import get_unit_of_work

    def override_uow() -> PostgresUnitOfWork:
        def mock_factory() -> AsyncSession:
            return db_session

        return PostgresUnitOfWork(session_factory=mock_factory)  # type: ignore

    app.dependency_overrides[get_unit_of_work] = override_uow
    return app


@pytest.mark.asyncio
async def test_create_and_get_reservation_api(
    test_app: FastAPI, db_session: AsyncSession
) -> None:
    """Verifies that endpoints can place and retrieve bookings."""
    # Seed DB
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.flush()

    room = Room(room_number="101", category_id=cat.id, status="Available")
    guest = Guest(first_name="Alexandra", last_name="Smith", email="alex@gmail.com")
    db_session.add_all([room, guest])
    await db_session.flush()

    # Place reservation POST /
    payload = {
        "guest_id": str(guest.id),
        "room_category_id": str(cat.id),
        "check_in_date": str(date.today() + timedelta(days=1)),
        "check_out_date": str(date.today() + timedelta(days=5)),
    }

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        response = await client.post("/", json=payload)
        assert response.status_code == 201, f"Err: {response.text}"
        data = response.json()
        assert data["success"] is True
        res_id = data["data"]["id"]

        # Retrieve reservation GET /{id}
        get_response = await client.get(f"/{res_id}")
        assert get_response.status_code == 200
        res_data = get_response.json()
        assert res_data["success"] is True
        assert res_data["data"]["status"] == "Confirmed"
        assert res_data["data"]["assigned_room_id"] == str(room.id)


@pytest.mark.asyncio
async def test_cancel_reservation_api(
    test_app: FastAPI, db_session: AsyncSession
) -> None:
    """Verifies API cancellation endpoint cancels booking and releases room."""
    cat = RoomCategory(name="Suite", base_price=300.00)
    db_session.add(cat)
    await db_session.flush()

    room = Room(room_number="301", category_id=cat.id, status="Available")
    guest = Guest(first_name="Diana", last_name="Prince", email="diana@temyscira.gov")
    db_session.add_all([room, guest])
    await db_session.flush()

    # Place reservation POST /
    payload = {
        "guest_id": str(guest.id),
        "room_category_id": str(cat.id),
        "check_in_date": str(date.today() + timedelta(days=5)),
        "check_out_date": str(date.today() + timedelta(days=10)),
    }

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        response = await client.post("/", json=payload)
        assert response.status_code == 201, f"Err: {response.text}"
        res_id = response.json()["data"]["id"]

        # Cancel reservation DELETE /{id}
        cancel_payload = {"reason": "Change of plans."}
        del_response = await client.request("DELETE", f"/{res_id}", json=cancel_payload)
        assert del_response.status_code == 200
        assert del_response.json()["success"] is True
        assert "Penalty applied: $0.00" in del_response.json()["message"]
