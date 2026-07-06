from datetime import timedelta
from typing import Any
from uuid import UUID

from sqlalchemy import select

from backend.models.reservation import Reservation
from backend.models.room import Room
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.reservation.domain.value_objects import BookingWindow


class AvailabilityEngine:
    """Calculates room inventory, checks collisions, and suggests booking alternatives."""

    async def check_category_availability(
        self, uow: AbstractUnitOfWork, category_id: UUID, window: BookingWindow
    ) -> bool:
        """Returns True if there is at least one room capacity available for every night in window."""
        # 1. Get all active rooms in this category
        rooms = await uow.rooms.get_by_category(str(category_id))
        total_rooms = len(rooms)
        if total_rooms == 0:
            return False

        # 2. Get active bookings in this category overlapping the window
        stmt = select(Reservation).filter(
            Reservation.room_category_id == category_id,
            Reservation.status.notin_(["Cancelled", "CheckedOut", "Completed"]),
            Reservation.is_deleted.is_(False),
            Reservation.check_in_date < window.check_out_date,
            Reservation.check_out_date > window.check_in_date,
        )
        res = await uow.session.execute(stmt)
        active_bookings = res.scalars().all()

        # 3. Check nightly capacity
        current_date = window.check_in_date
        while current_date < window.check_out_date:
            occupied_count = sum(
                1
                for b in active_bookings
                if b.check_in_date <= current_date < b.check_out_date
            )
            if occupied_count >= total_rooms:
                return False
            current_date += timedelta(days=1)

        return True

    async def get_available_rooms(
        self,
        uow: AbstractUnitOfWork,
        window: BookingWindow,
        category_id: UUID | None = None,
        preferences: dict[str, Any] | None = None,
    ) -> list[Room]:
        """Lists specific physical rooms that have no overlapping assignments during the window."""
        # 1. Fetch rooms
        if category_id:
            rooms = await uow.rooms.get_by_category(str(category_id))
        else:
            rooms = await uow.rooms.get_all()

        # 2. Get active bookings that are assigned to physical rooms and overlap
        stmt = select(Reservation).filter(
            Reservation.assigned_room_id.isnot(None),
            Reservation.status.notin_(["Cancelled", "CheckedOut", "Completed"]),
            Reservation.is_deleted.is_(False),
            Reservation.check_in_date < window.check_out_date,
            Reservation.check_out_date > window.check_in_date,
        )
        res = await uow.session.execute(stmt)
        overlapping_bookings = res.scalars().all()

        assigned_room_ids = {b.assigned_room_id for b in overlapping_bookings}

        # 3. Filter out occupied rooms
        available = [
            r
            for r in rooms
            if r.id not in assigned_room_ids and r.status == "Available"
        ]

        # 4. Optional preference filter (stub/heuristic matching)
        if preferences:
            # Stub: can filter or sort by preferences
            pass

        return available

    async def suggest_alternatives(
        self,
        uow: AbstractUnitOfWork,
        requested_category_id: UUID,
        window: BookingWindow,
    ) -> list[dict[str, Any]]:
        """Generates alternative room categories or shifts the date range if requested is full."""
        alternatives = []

        # Alternative 1: Check other room categories for the same dates
        categories = await uow.room_categories.get_all()
        for cat in categories:
            if cat.id != requested_category_id:
                has_space = await self.check_category_availability(uow, cat.id, window)
                if has_space:
                    alternatives.append(
                        {
                            "type": "alternative_category",
                            "room_category_id": cat.id,
                            "category_name": cat.name,
                            "check_in_date": window.check_in_date,
                            "check_out_date": window.check_out_date,
                            "price_factor": "standard",
                        }
                    )

        # Alternative 2: Shift check-in forward by 2 days, 4 days, or 7 days
        shifts = [2, 4, 7]
        for s in shifts:
            new_in = window.check_in_date + timedelta(days=s)
            new_out = window.check_out_date + timedelta(days=s)
            shifted_window = BookingWindow(check_in_date=new_in, check_out_date=new_out)
            has_space = await self.check_category_availability(
                uow, requested_category_id, shifted_window
            )
            if has_space:
                alternatives.append(
                    {
                        "type": "shifted_dates",
                        "room_category_id": requested_category_id,
                        "check_in_date": new_in,
                        "check_out_date": new_out,
                        "price_factor": "standard",
                    }
                )
            if len(alternatives) >= 3:
                break

        return alternatives[:3]


__all__ = ["AvailabilityEngine"]
