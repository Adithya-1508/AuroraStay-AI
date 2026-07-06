from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field
from sqlalchemy import select

from backend.ai.tools.executor import BaseTool
from backend.models.guest import Guest
from backend.models.reservation import Reservation
from backend.models.room import RoomCategory
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.reservation.domain.value_objects import BookingWindow
from business.reservation.services.availability import AvailabilityService
from business.reservation.services.cancellation import CancellationService
from business.reservation.services.pricing import PricingService
from business.reservation.services.reservation import ReservationService

# --- Input Schemas ---


class SearchAvailabilityInput(BaseModel):
    check_in_date: date = Field(..., description="Check-in date (YYYY-MM-DD)")
    check_out_date: date = Field(..., description="Check-out date (YYYY-MM-DD)")
    category_name: str | None = Field(
        None, description="Standard, Deluxe, Suite, Executive Suite"
    )


class CalculatePriceInput(BaseModel):
    category_name: str = Field(..., description="Room category name")
    check_in_date: date = Field(..., description="YYYY-MM-DD")
    check_out_date: date = Field(..., description="YYYY-MM-DD")
    guest_email: str = Field(..., description="Guest email to resolve loyalty tier")
    promo_code: str | None = Field(None, description="Optional discount promo code")


class ReserveRoomInput(BaseModel):
    guest_email: str = Field(..., description="Guest email address")
    category_name: str = Field(..., description="Standard, Deluxe, Suite, etc.")
    check_in_date: date = Field(..., description="YYYY-MM-DD")
    check_out_date: date = Field(..., description="YYYY-MM-DD")
    special_requests: str | None = Field(
        None, description="Preferences or pillow request"
    )
    promo_code: str | None = Field(None, description="Discount promo code")


class ModifyReservationInput(BaseModel):
    reservation_id: UUID = Field(..., description="UUID of the reservation to modify")
    check_in_date: date | None = Field(
        None, description="New check-in date (YYYY-MM-DD)"
    )
    check_out_date: date | None = Field(
        None, description="New check-out date (YYYY-MM-DD)"
    )
    category_name: str | None = Field(None, description="New room category name")


class CancelReservationInput(BaseModel):
    reservation_id: UUID = Field(..., description="UUID of the reservation to cancel")
    reason: str = Field(..., description="Detailed cancellation reason")


class RecommendUpgradeInput(BaseModel):
    reservation_id: UUID = Field(..., description="UUID of the reservation")


# --- Tool Implementations ---


class SearchAvailabilityTool(BaseTool):
    name = "SearchAvailabilityTool"
    description = "Searches for room category availability and alternative options for specified date ranges."
    args_schema = SearchAvailabilityInput

    async def _run(self, **kwargs: Any) -> Any:
        check_in = kwargs["check_in_date"]
        check_out = kwargs["check_out_date"]
        category_name = kwargs.get("category_name")
        window = BookingWindow(check_in_date=check_in, check_out_date=check_out)

        async with PostgresUnitOfWork() as uow:
            avail_service = AvailabilityService()

            # If specific category name is provided
            if category_name:
                stmt = select(RoomCategory).filter_by(
                    name=category_name.strip(), is_deleted=False
                )
                res = await uow.session.execute(stmt)
                cat = res.scalar_one_or_none()
                if not cat:
                    return {
                        "available": False,
                        "message": f"Room category '{category_name}' not found.",
                    }

                available = await avail_service.check_category_availability(
                    uow, cat.id, window
                )
                if available:
                    return {
                        "available": True,
                        "category_name": cat.name,
                        "nightly_rate": float(cat.base_price),
                        "message": f"Category '{category_name}' is available.",
                    }
                else:
                    alternatives = await avail_service.suggest_alternatives(
                        uow, cat.id, window
                    )
                    return {
                        "available": False,
                        "message": f"Category '{category_name}' is sold out. Alternatives listed.",
                        "alternatives": [
                            {
                                "type": alt["type"],
                                "category_name": alt.get("category_name")
                                or category_name,
                                "check_in_date": str(alt["check_in_date"]),
                                "check_out_date": str(alt["check_out_date"]),
                            }
                            for alt in alternatives
                        ],
                    }

            # If no category provided, list all available
            categories = await uow.room_categories.get_all()
            available_list = []
            for cat in categories:
                is_avail = await avail_service.check_category_availability(
                    uow, cat.id, window
                )
                if is_avail:
                    available_list.append(
                        {"category": cat.name, "nightly_rate": float(cat.base_price)}
                    )

            return {
                "available": len(available_list) > 0,
                "available_categories": available_list,
                "message": "Availability check complete.",
            }


class CalculatePriceTool(BaseTool):
    name = "CalculatePriceTool"
    description = "Calculates stay pricing breakdown including seasonal rates and loyalty tier discounts."
    args_schema = CalculatePriceInput

    async def _run(self, **kwargs: Any) -> Any:
        cat_name = kwargs["category_name"]
        check_in = kwargs["check_in_date"]
        check_out = kwargs["check_out_date"]
        email = kwargs["guest_email"]
        promo = kwargs.get("promo_code")

        window = BookingWindow(check_in_date=check_in, check_out_date=check_out)

        async with PostgresUnitOfWork() as uow:
            # Resolve guest loyalty tier
            guest_stmt = select(Guest).filter_by(email=email, is_deleted=False)
            res_guest = await uow.session.execute(guest_stmt)
            guest = res_guest.scalar_one_or_none()
            loyalty = guest.loyalty_tier if guest else "Bronze"

            # Resolve category ID
            cat_stmt = select(RoomCategory).filter_by(
                name=cat_name.strip(), is_deleted=False
            )
            res_cat = await uow.session.execute(cat_stmt)
            cat = res_cat.scalar_one_or_none()
            if not cat:
                raise ValueError(f"Category '{cat_name}' not found.")

            pricing_service = PricingService()
            breakdown = await pricing_service.calculate_reservation_price(
                uow, str(cat.id), window, loyalty, promo
            )

            return {
                "category_name": cat_name,
                "loyalty_tier": loyalty,
                "nights": window.duration_nights,
                "base_subtotal": float(breakdown.base_subtotal),
                "seasonal_adjustments": float(breakdown.seasonal_adjustments),
                "weekend_adjustments": float(breakdown.weekend_adjustments),
                "loyalty_discount": float(breakdown.loyalty_discount),
                "promo_discount": float(breakdown.promo_discount),
                "tax": float(breakdown.tax),
                "total_price": float(breakdown.total),
            }


class ReserveRoomTool(BaseTool):
    name = "confirm_reservation"  # Starts with "confirm" to trigger human approval gate
    description = "Places a room booking. Requires approval confirmation check."
    args_schema = ReserveRoomInput

    async def _run(self, **kwargs: Any) -> Any:
        email = kwargs["guest_email"]
        cat_name = kwargs["category_name"]
        check_in = kwargs["check_in_date"]
        check_out = kwargs["check_out_date"]
        requests = kwargs.get("special_requests")
        promo = kwargs.get("promo_code")

        async with PostgresUnitOfWork() as uow:
            # 1. Resolve Guest ID
            guest_stmt = select(Guest).filter_by(email=email, is_deleted=False)
            res_guest = await uow.session.execute(guest_stmt)
            guest = res_guest.scalar_one_or_none()
            if not guest:
                raise ValueError(
                    f"No guest found with email '{email}'. Please create profile first."
                )

            # 2. Resolve Category ID
            cat_stmt = select(RoomCategory).filter_by(
                name=cat_name.strip(), is_deleted=False
            )
            res_cat = await uow.session.execute(cat_stmt)
            cat = res_cat.scalar_one_or_none()
            if not cat:
                raise ValueError(f"Room category '{cat_name}' not found.")

            # 3. Call ReservationService
            res_service = ReservationService()
            pref_dict = {"special_requests": requests} if requests else {}
            reservation = await res_service.create_reservation(
                uow,
                guest_id=guest.id,
                room_category_id=cat.id,
                check_in_date=check_in,
                check_out_date=check_out,
                promo_code=promo,
                preferences=pref_dict,
            )
            await uow.commit()

            return {
                "success": True,
                "reservation_id": str(reservation.id),
                "guest_name": f"{guest.first_name} {guest.last_name}",
                "status": reservation.status,
                "total_cost": reservation.total_cost,
                "message": f"Reservation created successfully in status '{reservation.status}'.",
            }


class ModifyReservationTool(BaseTool):
    name = (
        "confirm_modify_reservation"  # Starts with "confirm" to trigger approval node
    )
    description = (
        "Alters dates or category of an active booking. Requires approval checks."
    )
    args_schema = ModifyReservationInput

    async def _run(self, **kwargs: Any) -> Any:
        res_id = kwargs["reservation_id"]
        check_in = kwargs.get("check_in_date")
        check_out = kwargs.get("check_out_date")
        cat_name = kwargs.get("category_name")

        async with PostgresUnitOfWork() as uow:
            cat_id = None
            if cat_name:
                cat_stmt = select(RoomCategory).filter_by(
                    name=cat_name.strip(), is_deleted=False
                )
                res_cat = await uow.session.execute(cat_stmt)
                cat = res_cat.scalar_one_or_none()
                if not cat:
                    raise ValueError(f"Category '{cat_name}' not found.")
                cat_id = cat.id

            res_service = ReservationService()
            reservation = await res_service.modify_reservation(
                uow,
                reservation_id=res_id,
                check_in_date=check_in,
                check_out_date=check_out,
                room_category_id=cat_id,
            )
            await uow.commit()

            return {
                "success": True,
                "reservation_id": str(reservation.id),
                "status": reservation.status,
                "total_cost": reservation.total_cost,
                "check_in_date": str(reservation.check_in_date),
                "check_out_date": str(reservation.check_out_date),
                "message": "Reservation modified successfully.",
            }


class CancelReservationTool(BaseTool):
    name = (
        "confirm_cancel_reservation"  # Starts with "confirm" to trigger approval node
    )
    description = (
        "Cancels an active booking, releasing rooms and calculating penalties."
    )
    args_schema = CancelReservationInput

    async def _run(self, **kwargs: Any) -> Any:
        res_id = kwargs["reservation_id"]
        reason = kwargs["reason"]

        async with PostgresUnitOfWork() as uow:
            cancellation_service = CancellationService()
            penalty = await cancellation_service.cancel_reservation(
                uow, reservation_id=res_id, reason=reason
            )
            await uow.commit()

            return {
                "success": True,
                "reservation_id": str(res_id),
                "penalty_applied": float(penalty),
                "message": f"Reservation cancelled. Cancellation penalty: ${float(penalty):.2f}.",
            }


class RecommendUpgradeTool(BaseTool):
    name = "RecommendUpgradeTool"
    description = (
        "Analyzes active reservation and checks eligibility for VIP room upgrades."
    )
    args_schema = RecommendUpgradeInput

    async def _run(self, **kwargs: Any) -> Any:
        res_id = kwargs["reservation_id"]

        async with PostgresUnitOfWork() as uow:
            res_stmt = select(Reservation).filter_by(id=res_id, is_deleted=False)
            db_res = await uow.session.execute(res_stmt)
            res = db_res.scalar_one_or_none()
            if not res:
                return {"eligible": False, "reason": "Reservation not found."}

            guest = await uow.guests.get(str(res.guest_id))
            loyalty = guest.loyalty_tier if guest else "Bronze"

            if loyalty not in ("Gold", "Platinum"):
                return {
                    "eligible": False,
                    "loyalty_tier": loyalty,
                    "reason": "Only Gold and Platinum loyalty tier members are eligible for complimentary upgrades.",
                }

            # Check next category in hierarchy
            cat_stmt = select(RoomCategory).filter_by(id=res.room_category_id)
            res_cat = await uow.session.execute(cat_stmt)
            current_category = res_cat.scalar_one_or_none()

            upgrade_hierarchy = ["Standard", "Deluxe", "Suite", "Executive Suite"]
            if not current_category or current_category.name not in upgrade_hierarchy:
                return {
                    "eligible": False,
                    "reason": "Room category not eligible for upgrades.",
                }

            current_idx = upgrade_hierarchy.index(current_category.name)
            if current_idx + 1 >= len(upgrade_hierarchy):
                return {
                    "eligible": False,
                    "reason": "Already booked in highest available category.",
                }

            next_category_name = upgrade_hierarchy[current_idx + 1]

            # Verify availability in next category
            from business.reservation.availability.engine import AvailabilityEngine

            window = BookingWindow(
                check_in_date=res.check_in_date, check_out_date=res.check_out_date
            )
            stmt = select(RoomCategory).filter_by(
                name=next_category_name, is_deleted=False
            )
            res_cat = await uow.session.execute(stmt)
            next_category = res_cat.scalar_one_or_none()

            if next_category:
                avail_engine = AvailabilityEngine()
                available = await avail_engine.check_category_availability(
                    uow, next_category.id, window
                )
                if available:
                    return {
                        "eligible": True,
                        "loyalty_tier": loyalty,
                        "current_category": current_category.name,
                        "recommended_upgrade": next_category_name,
                        "reason": f"Available upgrade to '{next_category_name}' located for {loyalty} member.",
                    }

            return {
                "eligible": False,
                "reason": f"No vacant rooms found in upgraded category '{next_category_name}' for stay dates.",
            }


__all__ = [
    "SearchAvailabilityTool",
    "CalculatePriceTool",
    "ReserveRoomTool",
    "ModifyReservationTool",
    "CancelReservationTool",
    "RecommendUpgradeTool",
]
