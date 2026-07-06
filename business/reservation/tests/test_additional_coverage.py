from datetime import date, timedelta
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.guest import Guest
from backend.models.reservation import Reservation
from backend.models.room import Room, RoomCategory
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.reservation.allocation.engine import AllocationEngine
from business.reservation.api.routes import router as reservations_router
from business.reservation.domain.enums import ReservationStatus
from business.reservation.domain.exceptions import (
    InvalidDateError,
    InventoryExhaustedError,
    ReservationDomainError,
    ReservationNotFoundError,
    RoomNotAvailableError,
    TransitionValidationError,
)
from business.reservation.domain.value_objects import GuestPreferences
from business.reservation.services.notification import (
    LogNotificationSender,
    NotificationService,
)
from business.reservation.services.reservation import ReservationService
from business.reservation.workflows.tools import (
    CalculatePriceTool,
    CancelReservationTool,
    ModifyReservationTool,
    RecommendUpgradeTool,
    ReserveRoomTool,
    SearchAvailabilityTool,
)


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


@pytest.fixture(autouse=True)
def setup_uow_mock(monkeypatch: pytest.MonkeyPatch, db_session: AsyncSession):
    # Set up PostgresUnitOfWork mock factory globally for all tests in this file
    def mock_factory() -> AsyncSession:
        return db_session

    from backend.repositories.unit_of_work import PostgresUnitOfWork

    old_init = PostgresUnitOfWork.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, session_factory=mock_factory)

    monkeypatch.setattr(PostgresUnitOfWork, "__init__", new_init)


@pytest.mark.asyncio
async def test_allocation_engine_errors(db_session: AsyncSession) -> None:
    engine = AllocationEngine()
    uow = PostgresUnitOfWork()

    async with uow:
        with pytest.raises(ReservationNotFoundError):
            await engine.allocate_room(uow, uuid4())

        with pytest.raises(ReservationNotFoundError):
            await engine.release_room_allocation(uow, uuid4())


@pytest.mark.asyncio
async def test_allocation_engine_upgrades(db_session: AsyncSession) -> None:
    engine = AllocationEngine()
    uow = PostgresUnitOfWork()

    # Seed initial entities
    cat_std = RoomCategory(id=uuid4(), name="Standard", base_price=100.00)
    cat_dlx = RoomCategory(id=uuid4(), name="Deluxe", base_price=150.00)
    db_session.add_all([cat_std, cat_dlx])
    await db_session.flush()

    guest_vip = Guest(
        id=uuid4(),
        first_name="VIP",
        last_name="Guest",
        email="vip@gmail.com",
        loyalty_tier="Platinum",
    )
    guest_bronze = Guest(
        id=uuid4(),
        first_name="Bronze",
        last_name="Guest",
        email="bronze@gmail.com",
        loyalty_tier="Bronze",
    )
    db_session.add_all([guest_vip, guest_bronze])
    await db_session.flush()

    # Reserve standard (but no standard rooms created yet -> standard is sold out!)
    res_vip = Reservation(
        id=uuid4(),
        guest_id=guest_vip.id,
        room_category_id=cat_std.id,
        check_in_date=date.today() + timedelta(days=1),
        check_out_date=date.today() + timedelta(days=2),
        total_cost=100.0,
        status=ReservationStatus.PENDING,
    )
    res_bronze = Reservation(
        id=uuid4(),
        guest_id=guest_bronze.id,
        room_category_id=cat_std.id,
        check_in_date=date.today() + timedelta(days=1),
        check_out_date=date.today() + timedelta(days=2),
        total_cost=100.0,
        status=ReservationStatus.PENDING,
    )
    db_session.add_all([res_vip, res_bronze])
    await db_session.flush()

    # Add deluxe room only (available upgrade option)
    room_dlx = Room(
        id=uuid4(), room_number="201", category_id=cat_dlx.id, status="Available"
    )
    db_session.add(room_dlx)
    await db_session.flush()

    # Store IDs
    res_vip_id = res_vip.id
    res_bronze_id = res_bronze.id
    room_dlx_id = room_dlx.id

    await db_session.commit()

    # VIP should successfully upgrade to Deluxe room
    async with uow:
        upgraded_room = await engine.allocate_room(uow, res_vip_id)
        assert upgraded_room.id == room_dlx_id

        # Bronze guest should fail upgrade path and raise InventoryExhaustedError
        with pytest.raises(InventoryExhaustedError):
            await engine.allocate_room(uow, res_bronze_id)

        # Test release room allocation happy path
        await engine.release_room_allocation(uow, res_vip_id)


@pytest.mark.asyncio
async def test_tool_search_availability(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.commit()

    tool_search = SearchAvailabilityTool()
    res1 = await tool_search._run(
        check_in_date=date.today(),
        check_out_date=date.today() + timedelta(days=1),
        category_name="Standard",
    )
    assert res1["available"] is False

    res2 = await tool_search._run(
        check_in_date=date.today(),
        check_out_date=date.today() + timedelta(days=1),
        category_name="InvalidCategoryName",
    )
    assert res2["available"] is False
    assert "not found" in res2["message"]


@pytest.mark.asyncio
async def test_tool_search_availability_no_category(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.commit()

    tool_search = SearchAvailabilityTool()
    res = await tool_search._run(
        check_in_date=date.today(), check_out_date=date.today() + timedelta(days=1)
    )
    assert "available_categories" in res


@pytest.mark.asyncio
async def test_tool_search_availability_success(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.flush()
    room = Room(room_number="101", category_id=cat.id, status="Available")
    db_session.add(room)
    await db_session.commit()

    tool = SearchAvailabilityTool()
    res = await tool._run(
        check_in_date=date.today() + timedelta(days=1),
        check_out_date=date.today() + timedelta(days=2),
        category_name="Standard",
    )
    assert res["available"] is True
    assert res["category_name"] == "Standard"


@pytest.mark.asyncio
async def test_tool_calculate_price(db_session: AsyncSession) -> None:
    guest = Guest(
        first_name="Jane", last_name="Doe", email="jane@gmail.com", loyalty_tier="Gold"
    )
    db_session.add(guest)
    await db_session.commit()

    tool_price = CalculatePriceTool()
    with pytest.raises(ValueError, match="not found"):
        await tool_price._run(
            category_name="UnknownCat",
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=1),
            guest_email="jane@gmail.com",
        )


@pytest.mark.asyncio
async def test_tool_calculate_price_success(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    guest = Guest(
        first_name="Jane", last_name="Doe", email="jane@gmail.com", loyalty_tier="Gold"
    )
    db_session.add_all([cat, guest])
    await db_session.commit()

    tool = CalculatePriceTool()
    res = await tool._run(
        category_name="Standard",
        check_in_date=date.today() + timedelta(days=1),
        check_out_date=date.today() + timedelta(days=2),
        guest_email="jane@gmail.com",
    )
    assert res["total_price"] > 0


@pytest.mark.asyncio
async def test_tool_reserve_room(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    guest = Guest(
        first_name="Jane", last_name="Doe", email="jane@gmail.com", loyalty_tier="Gold"
    )
    db_session.add_all([cat, guest])
    await db_session.commit()

    tool_reserve = ReserveRoomTool()
    with pytest.raises(ValueError, match="Please create profile first"):
        await tool_reserve._run(
            guest_email="nonexistent@gmail.com",
            category_name="Standard",
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=1),
        )

    with pytest.raises(ValueError, match="not found"):
        await tool_reserve._run(
            guest_email="jane@gmail.com",
            category_name="UnknownCat",
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=1),
        )


@pytest.mark.asyncio
async def test_tool_reserve_room_success(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    guest = Guest(
        first_name="Jane", last_name="Doe", email="jane@gmail.com", loyalty_tier="Gold"
    )
    db_session.add_all([cat, guest])
    await db_session.flush()
    room = Room(room_number="101", category_id=cat.id, status="Available")
    db_session.add(room)
    await db_session.commit()

    tool = ReserveRoomTool()
    res = await tool._run(
        guest_email="jane@gmail.com",
        category_name="Standard",
        check_in_date=date.today() + timedelta(days=1),
        check_out_date=date.today() + timedelta(days=2),
    )
    assert res["success"] is True


@pytest.mark.asyncio
async def test_tool_modify_reservation(db_session: AsyncSession) -> None:
    tool_modify = ModifyReservationTool()
    with pytest.raises(ValueError, match="not found"):
        await tool_modify._run(reservation_id=uuid4(), category_name="UnknownCat")


@pytest.mark.asyncio
async def test_tool_modify_reservation_success(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    guest = Guest(
        first_name="Jane", last_name="Doe", email="jane@gmail.com", loyalty_tier="Gold"
    )
    db_session.add_all([cat, guest])
    await db_session.flush()
    room = Room(room_number="101", category_id=cat.id, status="Available")
    db_session.add(room)
    await db_session.commit()

    uow = PostgresUnitOfWork()
    async with uow:
        res_service = ReservationService()
        res = await res_service.create_reservation(
            uow,
            guest_id=guest.id,
            room_category_id=cat.id,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=2),
        )
        await uow.commit()
        res_id = res.id

    tool = ModifyReservationTool()
    res_mod = await tool._run(
        reservation_id=res_id,
        category_name="Standard",
        check_in_date=date.today() + timedelta(days=2),
        check_out_date=date.today() + timedelta(days=4),
    )
    assert res_mod["success"] is True


@pytest.mark.asyncio
async def test_tool_cancel_reservation_success(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    guest = Guest(
        first_name="Jane", last_name="Doe", email="jane@gmail.com", loyalty_tier="Gold"
    )
    db_session.add_all([cat, guest])
    await db_session.flush()
    room = Room(room_number="101", category_id=cat.id, status="Available")
    db_session.add(room)
    await db_session.commit()

    uow = PostgresUnitOfWork()
    async with uow:
        res_service = ReservationService()
        res = await res_service.create_reservation(
            uow,
            guest_id=guest.id,
            room_category_id=cat.id,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=2),
        )
        await uow.commit()
        res_id = res.id

    tool = CancelReservationTool()
    res_cancel = await tool._run(reservation_id=res_id, reason="Changed my mind")
    assert res_cancel["success"] is True


@pytest.mark.asyncio
async def test_tool_recommend_upgrade_success(db_session: AsyncSession) -> None:
    cat_std = RoomCategory(name="Standard", base_price=100.00)
    cat_dlx = RoomCategory(name="Deluxe", base_price=150.00)
    guest = Guest(
        first_name="Jane",
        last_name="Doe",
        email="jane@gmail.com",
        loyalty_tier="Platinum",
    )
    db_session.add_all([cat_std, cat_dlx, guest])
    await db_session.flush()

    room_std = Room(room_number="101", category_id=cat_std.id, status="Available")
    room_dlx = Room(room_number="201", category_id=cat_dlx.id, status="Available")
    db_session.add_all([room_std, room_dlx])
    await db_session.commit()

    uow = PostgresUnitOfWork()
    async with uow:
        res_service = ReservationService()
        res = await res_service.create_reservation(
            uow,
            guest_id=guest.id,
            room_category_id=cat_std.id,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=2),
        )
        await uow.commit()
        res_id = res.id

    tool = RecommendUpgradeTool()
    res_up = await tool._run(reservation_id=res_id)
    assert res_up["eligible"] is True
    assert res_up["recommended_upgrade"] == "Deluxe"


@pytest.mark.asyncio
async def test_tool_recommend_upgrade_edge_cases(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    guest_bronze = Guest(
        first_name="Bronze",
        last_name="Doe",
        email="bronze@gmail.com",
        loyalty_tier="Bronze",
    )
    db_session.add_all([cat, guest_bronze])
    await db_session.commit()

    res_obj = Reservation(
        guest_id=guest_bronze.id,
        room_category_id=cat.id,
        check_in_date=date.today(),
        check_out_date=date.today() + timedelta(days=2),
        total_cost=200.0,
        status=ReservationStatus.CONFIRMED,
    )
    db_session.add(res_obj)
    await db_session.commit()

    tool_upgrade = RecommendUpgradeTool()

    # 1. Non-existent reservation upgrade check
    res_err = await tool_upgrade._run(reservation_id=uuid4())
    assert res_err["eligible"] is False
    assert "not found" in res_err["reason"]

    # 2. Bronze user upgrade check (fails loyalty check)
    res_up = await tool_upgrade._run(reservation_id=res_obj.id)
    assert res_up["eligible"] is False
    assert "loyalty" in res_up["reason"]


@pytest.mark.asyncio
async def test_notification_service() -> None:
    sender = LogNotificationSender()
    svc = NotificationService(sender=sender)

    details = {
        "reservation_id": "123-abc",
        "category_name": "Standard",
        "check_in_date": "2026-07-01",
        "check_out_date": "2026-07-05",
        "total_cost": 400.0,
        "room_number": "101",
    }

    # Test all with phone
    await svc.send_reservation_confirmation("Jane", "jane@gmail.com", "123456", details)
    await svc.send_reservation_reminder("Jane", "jane@gmail.com", "123456", details)
    await svc.send_reservation_cancellation(
        "Jane", "jane@gmail.com", "123456", details, "Reason"
    )
    await svc.send_reservation_modification(
        "Jane", "jane@gmail.com", "123456", details, "2026-07-01 to 2026-07-04"
    )
    await svc.send_check_in_confirmation("Jane", "jane@gmail.com", "123456", details)
    await svc.send_check_out_confirmation("Jane", "jane@gmail.com", "123456", details)
    await svc.send_ai_concierge_notification(
        "Jane", "jane@gmail.com", "123456", "Hello"
    )

    # Test all without phone
    await svc.send_reservation_confirmation("Jane", "jane@gmail.com", None, details)
    await svc.send_reservation_reminder("Jane", "jane@gmail.com", None, details)
    await svc.send_reservation_cancellation(
        "Jane", "jane@gmail.com", None, details, "Reason"
    )
    await svc.send_reservation_modification(
        "Jane", "jane@gmail.com", None, details, "2026-07-01 to 2026-07-04"
    )
    await svc.send_check_in_confirmation("Jane", "jane@gmail.com", None, details)
    await svc.send_check_out_confirmation("Jane", "jane@gmail.com", None, details)
    await svc.send_ai_concierge_notification("Jane", "jane@gmail.com", None, "Hello")


@pytest.mark.asyncio
async def test_reservation_service_transitions(db_session: AsyncSession) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.commit()

    room = Room(room_number="101", category_id=cat.id, status="Available")
    guest = Guest(first_name="Jane", last_name="Doe", email="jane@gmail.com")
    db_session.add_all([room, guest])
    await db_session.commit()

    res_service = ReservationService()
    uow = PostgresUnitOfWork()

    # 1. Create reservation
    async with uow:
        res = await res_service.create_reservation(
            uow,
            guest_id=guest.id,
            room_category_id=cat.id,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=2),
        )
        assert res.status == ReservationStatus.CONFIRMED

        # Test Check-in without assigned room id
        res.assigned_room_id = None
        await uow.reservations.update(res)
        await uow.session.flush()

        # Re-checking in will allocate the room automatically
        await res_service.check_in(uow, res.id, changed_by="Agent")
        assert res.status == ReservationStatus.CHECKED_IN

        # Test Check-out transitions
        await res_service.check_out(uow, res.id, changed_by="Agent")
        assert res.status == ReservationStatus.CHECKED_OUT

        # Test Complete transitions
        await res_service.complete_reservation(uow, res.id)
        assert res.status == ReservationStatus.COMPLETED

        # Test illegal transition validation error
        with pytest.raises(TransitionValidationError):
            await res_service.check_in(uow, res.id, changed_by="Agent")


@pytest.mark.asyncio
async def test_reservation_service_errors(db_session: AsyncSession) -> None:
    res_service = ReservationService()
    uow = PostgresUnitOfWork()

    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.flush()

    room = Room(room_number="101", category_id=cat.id, status="Available")
    guest = Guest(first_name="Jane", last_name="Doe", email="jane@gmail.com")
    db_session.add_all([room, guest])
    await db_session.commit()

    # 1. Invalid date error (past checkin)
    async with uow:
        with pytest.raises(InvalidDateError):
            await res_service.create_reservation(
                uow,
                guest_id=guest.id,
                room_category_id=cat.id,
                check_in_date=date.today() - timedelta(days=1),
                check_out_date=date.today(),
            )

        # Reservation not found during modify
        with pytest.raises(ReservationNotFoundError):
            await res_service.modify_reservation(uow, reservation_id=uuid4())

        # Complete non-existent reservation
        with pytest.raises(ReservationNotFoundError):
            await res_service.complete_reservation(uow, reservation_id=uuid4())


@pytest.mark.asyncio
async def test_reservation_service_edge_cases(db_session: AsyncSession) -> None:
    gp_none = GuestPreferences.from_dict(None)
    assert gp_none.pillow_type is None
    gp_val = GuestPreferences.from_dict({"pillow": "feather", "temp": "21C"})
    assert gp_val.pillow_type == "feather"

    res_service = ReservationService()
    uow = PostgresUnitOfWork()

    cat = RoomCategory(name="Standard", base_price=100.00)
    guest = Guest(first_name="Jane", last_name="Doe", email="jane@gmail.com")
    db_session.add_all([cat, guest])
    await db_session.commit()

    # 2. RoomNotAvailableError in create_reservation (no rooms added yet)
    async with uow:
        with pytest.raises(RoomNotAvailableError):
            await res_service.create_reservation(
                uow,
                guest_id=guest.id,
                room_category_id=cat.id,
                check_in_date=date.today() + timedelta(days=1),
                check_out_date=date.today() + timedelta(days=3),
            )

    # Add standard room
    room = Room(room_number="101", category_id=cat.id, status="Available")
    db_session.add(room)
    await db_session.commit()

    # 3. Create a reservation
    async with uow:
        res = await res_service.create_reservation(
            uow,
            guest_id=guest.id,
            room_category_id=cat.id,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3),
        )
        await uow.commit()
        res_id = res.id

    # 4. modify_reservation invalid status (e.g. modify a Completed reservation)
    async with uow:
        res_db = await uow.reservations.get(str(res_id))
        res_db.status = ReservationStatus.COMPLETED
        await uow.reservations.update(res_db)
        await uow.session.flush()

        with pytest.raises(TransitionValidationError):
            await res_service.modify_reservation(
                uow,
                reservation_id=res_id,
                check_in_date=date.today() + timedelta(days=5),
            )

        # Restore status
        res_db.status = ReservationStatus.CONFIRMED
        await uow.reservations.update(res_db)
        await uow.session.flush()

    # 5. modify_reservation invalid dates
    async with uow:
        with pytest.raises(InvalidDateError):
            await res_service.modify_reservation(
                uow,
                reservation_id=res_id,
                check_in_date=date.today() - timedelta(days=10),
            )

    # 6. check_in room not assigned and allocation engine fails (delete all standard rooms)
    async with uow:
        res_db = await uow.reservations.get(str(res_id))
        res_db.assigned_room_id = None
        await uow.reservations.update(res_db)
        # Delete rooms
        rooms = await uow.rooms.get_all()
        for r in rooms:
            await db_session.delete(r)
        await uow.session.flush()

        with pytest.raises(InventoryExhaustedError):
            await res_service.check_in(uow, res_id)

    # 7. check_in room not found in DB
    async with uow:
        res_db = await uow.reservations.get(str(res_id))
        res_db.assigned_room_id = uuid4()
        res_db.status = ReservationStatus.CONFIRMED
        await uow.reservations.update(res_db)
        await uow.session.flush()

        # check_in will see assigned_room_id but won't find it in rooms DB, so it should run without error but not mark as occupied
        await res_service.check_in(uow, res_id)
        assert res_db.status == ReservationStatus.CHECKED_IN

    # 8. check_out invalid status transition
    async with uow:
        res_db = await uow.reservations.get(str(res_id))
        res_db.status = ReservationStatus.COMPLETED
        await uow.reservations.update(res_db)
        await uow.session.flush()
        with pytest.raises(TransitionValidationError):
            await res_service.check_out(uow, res_id)

    # 9. complete_reservation invalid status transition
    async with uow:
        res_db = await uow.reservations.get(str(res_id))
        res_db.status = ReservationStatus.CONFIRMED
        await uow.reservations.update(res_db)
        await uow.session.flush()
        with pytest.raises(TransitionValidationError):
            await res_service.complete_reservation(uow, res_id)


@pytest.mark.asyncio
async def test_api_routes_invalid_dates(
    test_app: FastAPI, db_session: AsyncSession
) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.flush()
    cat_id = str(cat.id)

    room = Room(room_number="101", category_id=cat.id, status="Available")
    guest = Guest(first_name="Jane", last_name="Doe", email="jane@gmail.com")
    db_session.add_all([room, guest])
    await db_session.flush()
    guest_id = str(guest.id)

    await db_session.commit()

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        # GET non-existent reservation
        resp = await client.get(f"/{uuid4()}")
        assert resp.status_code == 404

        # POST / with ReservationDomainError due to invalid dates
        payload_invalid = {
            "guest_id": guest_id,
            "room_category_id": cat_id,
            "check_in_date": str(date.today() + timedelta(days=5)),
            "check_out_date": str(
                date.today() + timedelta(days=2)
            ),  # checkout before checkin!
        }
        resp = await client.post("/", json=payload_invalid)
        assert resp.status_code == 400


@pytest.mark.asyncio
async def test_api_routes_valid_flows(
    test_app: FastAPI, db_session: AsyncSession
) -> None:
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.flush()
    cat_id = str(cat.id)

    room = Room(room_number="101", category_id=cat.id, status="Available")
    guest = Guest(first_name="Jane", last_name="Doe", email="jane@gmail.com")
    db_session.add_all([room, guest])
    await db_session.flush()
    guest_id = str(guest.id)

    await db_session.commit()

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        # Create a valid one
        payload = {
            "guest_id": guest_id,
            "room_category_id": cat_id,
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3)),
        }
        resp_create = await client.post("/", json=payload)
        assert resp_create.status_code == 201, f"Err: {resp_create.text}"
        res_id = resp_create.json()["data"]["id"]

        # GET reservation by ID
        resp_get = await client.get(f"/{res_id}")
        assert resp_get.status_code == 200
        assert resp_get.json()["data"]["id"] == res_id

        # PUT modify reservation
        payload_modify = {
            "check_in_date": str(date.today() + timedelta(days=2)),
            "check_out_date": str(date.today() + timedelta(days=4)),
        }
        resp_mod = await client.put(f"/{res_id}", json=payload_modify)
        assert resp_mod.status_code == 200
        assert resp_mod.json()["success"] is True

        # Create another one for cancellation check
        payload_cancel = {
            "guest_id": guest_id,
            "room_category_id": cat_id,
            "check_in_date": str(date.today() + timedelta(days=5)),
            "check_out_date": str(date.today() + timedelta(days=8)),
        }
        resp_create2 = await client.post("/", json=payload_cancel)
        assert resp_create2.status_code == 201
        res_id2 = resp_create2.json()["data"]["id"]

        # POST availability check (overall list)
        avail_payload = {
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3)),
        }
        resp_avail = await client.post("/availability", json=avail_payload)
        assert resp_avail.status_code == 200
        assert "available_categories" in resp_avail.json()

        # POST availability check (specific category)
        avail_cat_payload = {
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3)),
            "room_category_id": cat_id,
        }
        resp_avail_cat = await client.post("/availability", json=avail_cat_payload)
        assert resp_avail_cat.status_code == 200
        assert "available" in resp_avail_cat.json()

        # DELETE cancel reservation
        cancel_payload = {"reason": "Change of travel plans."}
        resp_cancel = await client.request("DELETE", f"/{res_id2}", json=cancel_payload)
        assert resp_cancel.status_code == 200
        assert resp_cancel.json()["success"] is True


@pytest.mark.asyncio
async def test_api_chat_assistant(test_app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        chat_payload = {"session_id": "test-session-2", "message": "Hi"}
        resp = await client.post("/chat", json=chat_payload)
        assert resp.status_code == 200
        assert resp.json()["success"] is True


@pytest.mark.asyncio
async def test_api_routes_error_handling(
    test_app: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> None:
    from business.reservation.api.routes import get_unit_of_work

    assert get_unit_of_work() is not None

    # Directly invoke override_uow to cover get_unit_of_work / override_uow lines
    for override in test_app.dependency_overrides.values():
        res_uow = override()
        assert res_uow is not None

    from business.reservation.services.availability import AvailabilityService
    from business.reservation.services.cancellation import CancellationService
    from business.reservation.services.reservation import ReservationService

    async def mock_raise(*args, **kwargs):
        raise ReservationDomainError("Mock domain error")

    monkeypatch.setattr(ReservationService, "modify_reservation", mock_raise)
    monkeypatch.setattr(ReservationService, "create_reservation", mock_raise)
    monkeypatch.setattr(CancellationService, "cancel_reservation", mock_raise)
    monkeypatch.setattr(AvailabilityService, "check_category_availability", mock_raise)
    monkeypatch.setattr(AvailabilityService, "get_available_rooms", mock_raise)

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        # POST create domain error handler
        resp = await client.post(
            "/",
            json={
                "check_in_date": "2026-07-01",
                "check_out_date": "2026-07-02",
                "guest_id": str(uuid4()),
                "room_category_id": str(uuid4()),
            },
        )
        assert resp.status_code == 400

        # PUT modify domain error handler (400)
        resp = await client.put(f"/{uuid4()}", json={})
        assert resp.status_code == 400

        # DELETE cancellation domain error handler
        resp = await client.request(
            "DELETE", f"/{uuid4()}", json={"reason": "Test reason"}
        )
        assert resp.status_code == 400

        # POST availability check domain error handler
        resp = await client.post(
            "/availability",
            json={"check_in_date": "2026-07-01", "check_out_date": "2026-07-02"},
        )
        assert resp.status_code == 400

    async def mock_raise_generic(*args, **kwargs):
        raise Exception("Mock generic error")

    monkeypatch.setattr(ReservationService, "modify_reservation", mock_raise_generic)
    monkeypatch.setattr(ReservationService, "create_reservation", mock_raise_generic)
    monkeypatch.setattr(CancellationService, "cancel_reservation", mock_raise_generic)
    monkeypatch.setattr(
        AvailabilityService, "check_category_availability", mock_raise_generic
    )
    monkeypatch.setattr(AvailabilityService, "get_available_rooms", mock_raise_generic)

    async with AsyncClient(
        transport=ASGITransport(app=test_app), base_url="http://test"
    ) as client:
        # POST create generic error handler
        resp = await client.post(
            "/",
            json={
                "check_in_date": "2026-07-01",
                "check_out_date": "2026-07-02",
                "guest_id": str(uuid4()),
                "room_category_id": str(uuid4()),
            },
        )
        assert resp.status_code == 500

        # PUT modify generic error handler (500)
        resp = await client.put(f"/{uuid4()}", json={})
        assert resp.status_code == 500

        # DELETE cancellation generic error handler
        resp = await client.request(
            "DELETE", f"/{uuid4()}", json={"reason": "Test reason"}
        )
        assert resp.status_code == 500

        # POST availability check generic error handler
        resp = await client.post(
            "/availability",
            json={"check_in_date": "2026-07-01", "check_out_date": "2026-07-02"},
        )
        assert resp.status_code == 500
