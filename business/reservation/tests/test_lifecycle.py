from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.guest import Guest
from backend.models.room import Room, RoomCategory
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.reservation.domain.enums import ReservationStatus
from business.reservation.domain.exceptions import TransitionValidationError
from business.reservation.services.cancellation import CancellationService
from business.reservation.services.reservation import ReservationService


@pytest.mark.asyncio
async def test_reservation_full_lifecycle(db_session: AsyncSession) -> None:
    """Tests create, modify, check-in, check-out, and completion stay flows."""
    # 1. Setup seed
    cat = RoomCategory(name="Deluxe", base_price=200.00)
    db_session.add(cat)
    await db_session.flush()

    room = Room(room_number="201", category_id=cat.id, status="Available")
    guest = Guest(
        first_name="Gregory",
        last_name="House",
        email="house@princeton.org",
        loyalty_tier="Platinum",
    )
    db_session.add_all([room, guest])
    await db_session.flush()

    def mock_factory() -> AsyncSession:
        return db_session

    uow = PostgresUnitOfWork(session_factory=mock_factory)  # type: ignore

    res_service = ReservationService()

    # --- Step A: Create Reservation ---
    check_in = date(2026, 8, 1)
    check_out = date(2026, 8, 6)

    async with uow:
        res = await res_service.create_reservation(
            uow=uow,
            guest_id=guest.id,
            room_category_id=cat.id,
            check_in_date=check_in,
            check_out_date=check_out,
        )
        await uow.commit()

    assert res.id is not None
    assert res.status == ReservationStatus.CONFIRMED
    assert res.assigned_room_id == room.id
    # Price: 5 nights * 200 = 1000. Under Summer Peak (1.3x) + Weekend Premium (1.15x for Saturday).
    # Saturday: 200 * 1.3 * 1.15 = 299. Sun-Wed: 260 * 4 = 1040. Subtotal: 1339.
    # Platinum Discount (15%): 1138.15. Tax (12%): 136.578. Total: 1274.73
    assert float(res.total_cost) == 1274.73

    # Verify history entry
    async with uow:
        histories = await uow.reservation_histories.get_all()
        assert len(histories) >= 1
        assert histories[0].new_status == "Confirmed"

    # --- Step B: Modify Reservation ---
    new_in = date(2026, 8, 2)
    new_out = date(2026, 8, 5)  # 3 nights

    async with uow:
        res_mod = await res_service.modify_reservation(
            uow=uow,
            reservation_id=res.id,
            check_in_date=new_in,
            check_out_date=new_out,
        )
        await uow.commit()

    assert res_mod.check_in_date == new_in
    # Price: 3 nights * 200 = 600. Under Summer Peak (1.3x) -> 780.
    assert float(res_mod.total_cost) == 742.56

    # --- Step C: Check In ---
    # Temporarily set check_in date to today so validation/checks align if needed
    async with uow:
        res_db = await uow.reservations.get(str(res.id))
        assert res_db is not None
        # Move state to CheckedIn
        await res_service.check_in(uow, res_db.id)
        await uow.commit()

    assert res_db.status == ReservationStatus.CHECKED_IN
    # Verify room status
    async with uow:
        room_db = await uow.rooms.get(str(room.id))
        assert room_db is not None
        assert room_db.status == "Occupied"

    # --- Step D: Check Out ---
    async with uow:
        await res_service.check_out(uow, res_db.id)
        await uow.commit()

    assert res_db.status == ReservationStatus.CHECKED_OUT
    assert res_db.assigned_room_id is None
    # Verify room status is Dirty
    async with uow:
        room_db = await uow.rooms.get(str(room.id))
        assert room_db is not None
        assert room_db.status == "Dirty"


@pytest.mark.asyncio
async def test_cancellation_policy_penalty(db_session: AsyncSession) -> None:
    """Verifies that cancellation penalty is charged if check-in is < 24 hours away."""
    # 1. Setup seed
    cat = RoomCategory(name="Suite", base_price=300.00)
    db_session.add(cat)
    await db_session.flush()

    room = Room(room_number="301", category_id=cat.id, status="Available")
    guest = Guest(first_name="Diana", last_name="Prince", email="diana@temyscira.gov")
    db_session.add_all([room, guest])
    await db_session.flush()

    def mock_factory() -> AsyncSession:
        return db_session

    uow = PostgresUnitOfWork(session_factory=mock_factory)  # type: ignore

    res_service = ReservationService()
    cancel_service = CancellationService()

    # Check-in today (less than 24h away)
    async with uow:
        res = await res_service.create_reservation(
            uow=uow,
            guest_id=guest.id,
            room_category_id=cat.id,
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=3),
        )
        await uow.commit()

    # Cancel
    async with uow:
        penalty = await cancel_service.cancel_reservation(
            uow=uow,
            reservation_id=res.id,
            reason="Flight cancelled.",
        )
        await uow.commit()

    # Penalty should be 1 night base price (300.00)
    assert penalty == Decimal("300.00")
    assert res.status == ReservationStatus.CANCELLED

    # Check that checking in a cancelled reservation fails
    with pytest.raises(TransitionValidationError):
        async with uow:
            await res_service.check_in(uow, res.id)
