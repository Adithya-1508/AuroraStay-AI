from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.guest import Guest
from backend.models.reservation import Reservation
from backend.models.room import Room, RoomCategory


class DatabaseLoader:
    """ETL Database Loader inserting and upserting records in PostgreSQL."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def load_pms_records(self, records: list[dict[str, Any]]) -> int:
        """Loads and upserts guest, category, room, and reservation records."""
        loaded_count = 0

        for r in records:
            # 1. Fetch or create Guest profile
            email = r["guest_email"]
            stmt_guest = select(Guest).filter_by(email=email)
            res_guest = await self.session.execute(stmt_guest)
            guest = res_guest.scalar_one_or_none()

            if not guest:
                guest = Guest(
                    first_name=r["first_name"],
                    last_name=r["last_name"],
                    email=email,
                    phone=r["phone"],
                    loyalty_tier="Bronze",
                )
                self.session.add(guest)
                # Flush to assign guest ID
                await self.session.flush()

            # 2. Fetch or create RoomCategory profile
            category_name = r["room_category"]
            stmt_cat = select(RoomCategory).filter_by(name=category_name)
            res_cat = await self.session.execute(stmt_cat)
            category = res_cat.scalar_one_or_none()

            if not category:
                category = RoomCategory(
                    name=category_name,
                    base_price=350.00 if category_name == "Suite" else 150.00,
                )
                self.session.add(category)
                await self.session.flush()

            # 3. Fetch or create Room profile
            room_num = r["room_number"]
            stmt_room = select(Room).filter_by(room_number=room_num)
            res_room = await self.session.execute(stmt_room)
            room = res_room.scalar_one_or_none()

            if not room:
                room = Room(
                    room_number=room_num,
                    category_id=category.id,
                    status="Available",
                )
                self.session.add(room)
                await self.session.flush()

            # 4. Insert Reservation
            reservation = Reservation(
                guest_id=guest.id,
                room_category_id=category.id,
                assigned_room_id=room.id,
                check_in_date=r["check_in"],
                check_out_date=r["check_out"],
                total_cost=r["total_cost"],
                status=r["status"],
            )
            self.session.add(reservation)
            loaded_count += 1

        # Flush all final entries
        await self.session.flush()
        return loaded_count


__all__ = ["DatabaseLoader"]
