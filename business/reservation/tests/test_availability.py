from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.guest import Guest
from backend.models.reservation import Reservation
from backend.models.room import Room, RoomCategory
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.reservation.availability.engine import AvailabilityEngine
from business.reservation.domain.value_objects import BookingWindow


@pytest.mark.asyncio
async def test_availability_engine_checks(db_session: AsyncSession) -> None:
    """Verifies date overlap collision detection under AvailabilityEngine."""
    # 1. Seed database
    cat = RoomCategory(name="Standard", base_price=100.00)
    db_session.add(cat)
    await db_session.flush()

    room1 = Room(room_number="101", category_id=cat.id, status="Available")
    room2 = Room(room_number="102", category_id=cat.id, status="Available")
    guest = Guest(first_name="Alexandra", last_name="Smith", email="alex@gmail.com")
    db_session.add_all([room1, room2, guest])
    await db_session.flush()

    def mock_factory() -> AsyncSession:
        return db_session

    uow = PostgresUnitOfWork(session_factory=mock_factory)  # type: ignore

    engine = AvailabilityEngine()

    # Case A: Requested window [May 10, May 15). No active bookings.
    window = BookingWindow(
        check_in_date=date(2026, 5, 10), check_out_date=date(2026, 5, 15)
    )
    async with uow:
        is_avail = await engine.check_category_availability(uow, cat.id, window)
        assert is_avail is True

        available_rooms = await engine.get_available_rooms(
            uow, window, category_id=cat.id
        )
        assert len(available_rooms) == 2

    # Case B: Create 1 booking. Room category standard has 2 rooms, so 1 booking should still leave capacity.
    async with uow:
        res1 = Reservation(
            guest_id=guest.id,
            room_category_id=cat.id,
            assigned_room_id=room1.id,
            check_in_date=date(2026, 5, 10),
            check_out_date=date(2026, 5, 15),
            total_cost=500.00,
            status="Confirmed",
        )
        await uow.reservations.add(res1)
        await uow.commit()

    async with uow:
        is_avail = await engine.check_category_availability(uow, cat.id, window)
        assert is_avail is True  # 1 room left

        available_rooms = await engine.get_available_rooms(
            uow, window, category_id=cat.id
        )
        assert len(available_rooms) == 1
        assert available_rooms[0].room_number == "102"

    # Case C: Create a second overlapping booking. Now standard category is sold out for these dates.
    async with uow:
        res2 = Reservation(
            guest_id=guest.id,
            room_category_id=cat.id,
            assigned_room_id=room2.id,
            check_in_date=date(2026, 5, 12),
            check_out_date=date(2026, 5, 14),
            total_cost=200.00,
            status="Confirmed",
        )
        await uow.reservations.add(res2)
        await uow.commit()

    async with uow:
        # Check availability on overlapping window [10, 15) -> should be False because on May 12-14 both rooms are booked.
        is_avail = await engine.check_category_availability(uow, cat.id, window)
        assert is_avail is False

        # Check alternatives. Shifting dates should work since May 17+ has no bookings.
        alternatives = await engine.suggest_alternatives(uow, cat.id, window)
        assert len(alternatives) > 0
        assert alternatives[0]["type"] == "shifted_dates"
