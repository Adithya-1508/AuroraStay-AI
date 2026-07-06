import asyncio
from datetime import UTC, date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.session import async_session_factory
from backend.models.employee import Employee
from backend.models.guest import Guest
from backend.models.reservation import Reservation
from backend.models.review import Review
from backend.models.room import Room, RoomCategory
from backend.models.spa import Spa, SpaBooking


async def seed_database(session: AsyncSession) -> None:
    """Populates relational tables with realistic hotel operations data."""

    # 1. Seed Room Categories
    categories_data = [
        {"name": "Standard", "base_price": 120.00},
        {"name": "Deluxe", "base_price": 200.00},
        {"name": "Suite", "base_price": 380.00},
        {"name": "Executive Suite", "base_price": 650.00},
    ]
    categories = {}
    for data in categories_data:
        stmt = select(RoomCategory).filter_by(name=data["name"])
        res = await session.execute(stmt)
        cat = res.scalar_one_or_none()
        if not cat:
            cat = RoomCategory(name=data["name"], base_price=data["base_price"])
            session.add(cat)
            await session.flush()
        categories[data["name"]] = cat

    # 2. Seed Rooms
    rooms_data = [
        {"room_number": "101", "category": "Standard"},
        {"room_number": "102", "category": "Standard"},
        {"room_number": "201", "category": "Deluxe"},
        {"room_number": "202", "category": "Deluxe"},
        {"room_number": "301", "category": "Suite"},
        {"room_number": "401", "category": "Executive Suite"},
    ]
    rooms = {}
    for data in rooms_data:
        stmt = select(Room).filter_by(room_number=data["room_number"])
        res = await session.execute(stmt)
        room = res.scalar_one_or_none()
        if not room:
            room = Room(
                room_number=data["room_number"],
                category_id=categories[data["category"]].id,
                status="Available",
            )
            session.add(room)
            await session.flush()
        rooms[data["room_number"]] = room

    # 3. Seed Guests
    guests_data = [
        {
            "first_name": "Alexandra",
            "last_name": "Smith",
            "email": "alexandra.smith@gmail.com",
            "phone": "+1-555-0101",
            "loyalty_tier": "Gold",
            "preferences": {"temp": "72F", "pillow": "down"},
        },
        {
            "first_name": "Gregory",
            "last_name": "House",
            "email": "gregory.house@princeton.org",
            "phone": "+1-555-0303",
            "loyalty_tier": "Platinum",
            "preferences": {"temp": "68F", "pillow": "orthopedic"},
        },
        {
            "first_name": "Diana",
            "last_name": "Prince",
            "email": "diana.prince@temyscira.gov",
            "phone": "+1-555-1941",
            "loyalty_tier": "Gold",
            "preferences": {"temp": "70F"},
        },
    ]
    guests = {}
    for data in guests_data:
        stmt = select(Guest).filter_by(email=data["email"])
        res = await session.execute(stmt)
        guest = res.scalar_one_or_none()
        if not guest:
            guest = Guest(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone=data["phone"],
                loyalty_tier=data["loyalty_tier"],
                preferences=data["preferences"],
            )
            session.add(guest)
            await session.flush()
        guests[data["email"]] = guest

    # 4. Seed Employees
    employees_data = [
        {
            "first_name": "Michael",
            "last_name": "Scott",
            "email": "michael.scott@dundermifflin.com",
            "role": "Manager",
        },
        {
            "first_name": "Dwight",
            "last_name": "Schrute",
            "email": "dwight.schrute@dundermifflin.com",
            "role": "Housekeeper",
        },
    ]
    for data in employees_data:
        stmt = select(Employee).filter_by(email=data["email"])
        res = await session.execute(stmt)
        emp = res.scalar_one_or_none()
        if not emp:
            emp = Employee(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                role=data["role"],
            )
            session.add(emp)
            await session.flush()

    # 5. Seed Spas
    spas_data = [
        {"name": "Zen Massage", "treatment_type": "Massage", "duration_minutes": 60},
        {"name": "Royal Facial", "treatment_type": "Facial", "duration_minutes": 45},
    ]
    spas = {}
    for data in spas_data:
        stmt = select(Spa).filter_by(name=data["name"])
        res = await session.execute(stmt)
        spa = res.scalar_one_or_none()
        if not spa:
            spa = Spa(
                name=data["name"],
                treatment_type=data["treatment_type"],
                duration_minutes=data["duration_minutes"],
            )
            session.add(spa)
            await session.flush()
        spas[data["name"]] = spa

    # 6. Seed Reservations & Reviews & SpaBookings
    # Booking 1: Past stay for Alexandra
    stmt_res = (
        select(Reservation)
        .join(Guest)
        .filter(Guest.email == "alexandra.smith@gmail.com")
    )
    res_db = await session.execute(stmt_res)
    has_res = res_db.scalars().all()

    if not has_res:
        # Reservation
        res1 = Reservation(
            guest_id=guests["alexandra.smith@gmail.com"].id,
            room_category_id=categories["Standard"].id,
            assigned_room_id=rooms["101"].id,
            check_in_date=date.today() - timedelta(days=10),
            check_out_date=date.today() - timedelta(days=5),
            total_cost=600.00,
            status="CheckedOut",
        )
        session.add(res1)
        await session.flush()

        # Review
        rev1 = Review(
            reservation_id=res1.id,
            guest_id=guests["alexandra.smith@gmail.com"].id,
            score=5,
            content="Absolutely magnificent stay! Housekeeping was top notch.",
            submitted_at=datetime.now(UTC),
            sentiment="Positive",
        )
        session.add(rev1)

        # Spa Booking
        sb1 = SpaBooking(
            guest_id=guests["alexandra.smith@gmail.com"].id,
            spa_id=spas["Zen Massage"].id,
            booking_time=datetime.now(UTC) - timedelta(days=8),
            status="Completed",
        )
        session.add(sb1)

    await session.commit()


async def run_standalone_seeder() -> None:
    """Async main routine running seed task inside session factory."""
    async with async_session_factory() as session:
        await seed_database(session)


if __name__ == "__main__":
    asyncio.run(run_standalone_seeder())
