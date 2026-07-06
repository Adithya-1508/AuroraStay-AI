from datetime import date
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.reservation.domain.exceptions import ReservationDomainError
from business.reservation.services.availability import AvailabilityService
from business.reservation.services.cancellation import CancellationService
from business.reservation.services.reservation import ReservationService
from business.reservation.workflows.agent import ReservationAssistantAgent

router = APIRouter()


def get_unit_of_work() -> PostgresUnitOfWork:
    """Dependency injector resolving concrete PostgresUnitOfWork transactions."""
    return PostgresUnitOfWork()


# --- Request/Response Models ---


class CreateReservationRequest(BaseModel):
    guest_id: UUID
    room_category_id: UUID
    check_in_date: date
    check_out_date: date
    promo_code: str | None = None
    preferences: dict[str, Any] | None = None


class ModifyReservationRequest(BaseModel):
    check_in_date: date | None = None
    check_out_date: date | None = None
    room_category_id: UUID | None = None


class CancelReservationRequest(BaseModel):
    reason: str = Field(..., min_length=5)


class SearchAvailabilityRequest(BaseModel):
    check_in_date: date
    check_out_date: date
    room_category_id: UUID | None = None


class ChatRequest(BaseModel):
    session_id: str
    message: str
    thread_id: str | None = None


# --- Endpoints ---


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reservation(
    payload: CreateReservationRequest,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Places a new room booking reservation."""
    service = ReservationService()
    try:
        async with uow:
            res = await service.create_reservation(
                uow=uow,
                guest_id=payload.guest_id,
                room_category_id=payload.room_category_id,
                check_in_date=payload.check_in_date,
                check_out_date=payload.check_out_date,
                promo_code=payload.promo_code,
                preferences=payload.preferences,
            )
            await uow.commit()
            return {
                "success": True,
                "data": {
                    "id": str(res.id),
                    "guest_id": str(res.guest_id),
                    "room_category_id": str(res.room_category_id),
                    "assigned_room_id": str(res.assigned_room_id)
                    if res.assigned_room_id
                    else None,
                    "check_in_date": str(res.check_in_date),
                    "check_out_date": str(res.check_out_date),
                    "total_cost": float(res.total_cost),
                    "status": res.status,
                },
            }
    except ReservationDomainError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}"
        ) from e


@router.get("/{id}")
async def get_reservation(
    id: UUID,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Retrieves reservation details by unique identifier."""
    async with uow:
        res = await uow.reservations.get(str(id))
        if not res:
            raise HTTPException(status_code=404, detail="Reservation not found.")
        return {
            "success": True,
            "data": {
                "id": str(res.id),
                "guest_id": str(res.guest_id),
                "room_category_id": str(res.room_category_id),
                "assigned_room_id": str(res.assigned_room_id)
                if res.assigned_room_id
                else None,
                "check_in_date": str(res.check_in_date),
                "check_out_date": str(res.check_out_date),
                "total_cost": float(res.total_cost),
                "status": res.status,
            },
        }


@router.put("/{id}")
async def modify_reservation(
    id: UUID,
    payload: ModifyReservationRequest,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Alters stay dates or category of an active booking."""
    service = ReservationService()
    try:
        async with uow:
            res = await service.modify_reservation(
                uow=uow,
                reservation_id=id,
                check_in_date=payload.check_in_date,
                check_out_date=payload.check_out_date,
                room_category_id=payload.room_category_id,
            )
            await uow.commit()
            return {
                "success": True,
                "data": {
                    "id": str(res.id),
                    "check_in_date": str(res.check_in_date),
                    "check_out_date": str(res.check_out_date),
                    "room_category_id": str(res.room_category_id),
                    "assigned_room_id": str(res.assigned_room_id)
                    if res.assigned_room_id
                    else None,
                    "total_cost": float(res.total_cost),
                    "status": res.status,
                },
            }
    except ReservationDomainError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}"
        ) from e


@router.delete("/{id}")
async def cancel_reservation(
    id: UUID,
    payload: CancelReservationRequest,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Cancels booking, running refund policy checks and releasing room."""
    service = CancellationService()
    try:
        async with uow:
            penalty = await service.cancel_reservation(
                uow=uow,
                reservation_id=id,
                reason=payload.reason,
            )
            await uow.commit()
            return {
                "success": True,
                "message": f"Reservation cancelled successfully. Penalty applied: ${float(penalty):.2f}",
                "data": {"penalty_applied": float(penalty)},
            }
    except ReservationDomainError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}"
        ) from e


@router.post("/availability")
async def check_availability(
    payload: SearchAvailabilityRequest,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Queries availability of room category for dates."""
    service = AvailabilityService()
    from business.reservation.domain.value_objects import BookingWindow

    try:
        window = BookingWindow(
            check_in_date=payload.check_in_date, check_out_date=payload.check_out_date
        )
        async with uow:
            if payload.room_category_id:
                available = await service.check_category_availability(
                    uow, payload.room_category_id, window
                )
                return {"success": True, "available": available}
            else:
                rooms = await service.get_available_rooms(uow, window)
                categories = {str(r.category_id) for r in rooms}
                return {
                    "success": True,
                    "available_categories": list(categories),
                }
    except ReservationDomainError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {e}"
        ) from e


@router.post("/chat")
async def chat_assistant(
    payload: ChatRequest,
) -> dict[str, Any]:
    """Conversational endpoint routing natural language to the Reservation Assistant Agent."""
    agent = ReservationAssistantAgent()
    try:
        await agent.initialize()
        result = await agent.chat(
            session_id=payload.session_id,
            message=payload.message,
            thread_id=payload.thread_id,
        )
        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assistant chat error: {e}") from e


__all__ = ["router"]
