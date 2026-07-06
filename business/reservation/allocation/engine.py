from typing import Any
from uuid import UUID

from sqlalchemy import select

from backend.models.reservation import Reservation
from backend.models.room import Room, RoomCategory
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.reservation.domain.exceptions import (
    InventoryExhaustedError,
    ReservationNotFoundError,
)
from business.reservation.domain.value_objects import BookingWindow


class AllocationEngine:
    """Manages physical room assignments, respecting guest preferences and handling loyalty upgrades."""

    async def allocate_room(
        self,
        uow: AbstractUnitOfWork,
        reservation_id: UUID,
        preferences: dict[str, Any] | None = None,
    ) -> Room:
        """Assigns the best available room to the reservation, upgrading the guest if necessary."""
        # 1. Fetch reservation
        res_stmt = select(Reservation).filter_by(id=reservation_id, is_deleted=False)
        db_res = await uow.session.execute(res_stmt)
        reservation = db_res.scalar_one_or_none()
        if not reservation:
            raise ReservationNotFoundError(f"Reservation '{reservation_id}' not found.")

        window = BookingWindow(
            check_in_date=reservation.check_in_date,
            check_out_date=reservation.check_out_date,
        )

        # 2. Get guest loyalty
        guest = await uow.guests.get(str(reservation.guest_id))
        loyalty_tier = guest.loyalty_tier if guest else "Bronze"

        # 3. Find available rooms in the requested category
        from business.reservation.availability.engine import AvailabilityEngine

        avail_engine = AvailabilityEngine()

        available_rooms = await avail_engine.get_available_rooms(
            uow, window, category_id=reservation.room_category_id
        )

        if available_rooms:
            # Assign first available room (satisfying preferences can be added as sorting)
            assigned_room = available_rooms[0]
            reservation.assigned_room_id = assigned_room.id
            await uow.reservations.update(reservation)
            return assigned_room

        # 4. If requested category is sold out, evaluate Upgrade Paths
        category_stmt = select(RoomCategory).filter_by(id=reservation.room_category_id)
        db_cat = await uow.session.execute(category_stmt)
        req_category = db_cat.scalar_one_or_none()
        if not req_category:
            raise InventoryExhaustedError("Requested room category not found.")

        # Hierarchy: Standard -> Deluxe -> Suite -> Executive Suite
        upgrade_hierarchy = ["Standard", "Deluxe", "Suite", "Executive Suite"]
        if req_category.name not in upgrade_hierarchy:
            raise InventoryExhaustedError("Category not eligible for upgrades.")

        current_idx = upgrade_hierarchy.index(req_category.name)

        # Loyalty upgrade checks: VIP (Platinum/Gold) receive priority
        allow_upgrade = loyalty_tier in ("Gold", "Platinum")

        if allow_upgrade and current_idx + 1 < len(upgrade_hierarchy):
            next_category_name = upgrade_hierarchy[current_idx + 1]
            stmt = select(RoomCategory).filter_by(
                name=next_category_name, is_deleted=False
            )
            res_cat = await uow.session.execute(stmt)
            next_category = res_cat.scalar_one_or_none()

            if next_category:
                upgraded_rooms = await avail_engine.get_available_rooms(
                    uow, window, category_id=next_category.id
                )
                if upgraded_rooms:
                    assigned_room = upgraded_rooms[0]
                    reservation.assigned_room_id = assigned_room.id
                    # Note: We keep the original room_category_id on reservation so they are billed standard,
                    # but set assigned_room_id to the upgraded room! This is standard guest upgrade practice.
                    await uow.reservations.update(reservation)
                    return assigned_room

        raise InventoryExhaustedError(
            f"No physical rooms available for requested category '{req_category.name}' "
            f"and no upgrade path could be fulfilled."
        )

    async def release_room_allocation(
        self, uow: AbstractUnitOfWork, reservation_id: UUID
    ) -> None:
        """Clears the room assignment for a reservation."""
        res_stmt = select(Reservation).filter_by(id=reservation_id, is_deleted=False)
        db_res = await uow.session.execute(res_stmt)
        reservation = db_res.scalar_one_or_none()
        if not reservation:
            raise ReservationNotFoundError(f"Reservation '{reservation_id}' not found.")

        reservation.assigned_room_id = None
        await uow.reservations.update(reservation)


__all__ = ["AllocationEngine"]
