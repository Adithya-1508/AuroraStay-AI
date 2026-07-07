from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.ops.domain.exceptions import (
    EmployeeNotFoundError,
    MaintenanceRequestNotFoundError,
    OpsDomainError,
    RoomNotFoundError,
    TaskNotFoundError,
)
from business.ops.services.operations import OperationsService

router = APIRouter()
service = OperationsService()


def get_unit_of_work() -> PostgresUnitOfWork:
    """Dependency injector resolving concrete PostgresUnitOfWork transactions."""
    return PostgresUnitOfWork()


# --- Request Models ---


class HousekeepingTaskCreate(BaseModel):
    room_id: UUID


class HousekeepingTaskAssign(BaseModel):
    employee_id: UUID


class MaintenanceRequestCreate(BaseModel):
    room_id: UUID
    description: str
    priority: str = "LOW"


class MaintenanceRequestAssign(BaseModel):
    employee_id: UUID


# --- API Routes ---

# 1. Housekeeping Tasks


@router.get("/housekeeping/tasks", response_model=list[dict[str, Any]])
async def list_housekeeping_tasks(
    status_filter: str | None = None,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> list[dict[str, Any]]:
    """Returns a list of housekeeping tasks, optionally filtered by status."""
    async with uow:
        tasks = await service.list_housekeeping_tasks(uow, status_filter)
        return [
            {
                "id": str(t.id),
                "room_id": str(t.room_id),
                "assigned_employee_id": str(t.assigned_employee_id)
                if t.assigned_employee_id
                else None,
                "status": t.status,
                "created_at": t.created_at.isoformat(),
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            }
            for t in tasks
        ]


@router.post(
    "/housekeeping/tasks",
    response_model=dict[str, Any],
    status_code=status.HTTP_201_CREATED,
)
async def create_housekeeping_task(
    req: HousekeepingTaskCreate,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Manually creates a housekeeping task for a room."""
    try:
        async with uow:
            t = await service.create_housekeeping_task(uow, req.room_id)
            return {
                "id": str(t.id),
                "room_id": str(t.room_id),
                "assigned_employee_id": None,
                "status": t.status,
                "created_at": t.created_at.isoformat(),
                "completed_at": None,
            }
    except RoomNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.post("/housekeeping/tasks/{id}/assign", response_model=dict[str, Any])
async def assign_housekeeping_task(
    id: UUID,
    req: HousekeepingTaskAssign,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Assigns an employee to a housekeeping task."""
    try:
        async with uow:
            t = await service.assign_housekeeping_task(uow, id, req.employee_id)
            return {
                "id": str(t.id),
                "room_id": str(t.room_id),
                "assigned_employee_id": str(t.assigned_employee_id),
                "status": t.status,
                "created_at": t.created_at.isoformat(),
                "completed_at": None,
            }
    except (TaskNotFoundError, EmployeeNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.post("/housekeeping/tasks/{id}/complete", response_model=dict[str, Any])
async def complete_housekeeping_task(
    id: UUID,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Completes a housekeeping task."""
    try:
        async with uow:
            t = await service.complete_housekeeping_task(uow, id)
            return {
                "id": str(t.id),
                "room_id": str(t.room_id),
                "assigned_employee_id": str(t.assigned_employee_id),
                "status": t.status,
                "created_at": t.created_at.isoformat(),
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            }
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except OpsDomainError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e


# 2. Maintenance Requests


@router.get("/maintenance/requests", response_model=list[dict[str, Any]])
async def list_maintenance_requests(
    status_filter: str | None = None,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> list[dict[str, Any]]:
    """Returns a list of maintenance requests, optionally filtered by status."""
    async with uow:
        requests = await service.list_maintenance_requests(uow, status_filter)
        return [
            {
                "id": str(r.id),
                "room_id": str(r.room_id),
                "assigned_employee_id": str(r.assigned_employee_id)
                if r.assigned_employee_id
                else None,
                "status": r.status,
                "priority": r.priority,
                "description": r.description,
                "created_at": r.created_at.isoformat(),
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            }
            for r in requests
        ]


@router.post(
    "/maintenance/requests",
    response_model=dict[str, Any],
    status_code=status.HTTP_201_CREATED,
)
async def create_maintenance_request(
    req: MaintenanceRequestCreate,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Creates a maintenance request."""
    try:
        async with uow:
            r = await service.create_maintenance_request(
                uow, req.room_id, req.description, req.priority
            )
            return {
                "id": str(r.id),
                "room_id": str(r.room_id),
                "assigned_employee_id": None,
                "status": r.status,
                "priority": r.priority,
                "description": r.description,
                "created_at": r.created_at.isoformat(),
                "completed_at": None,
            }
    except RoomNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.post("/maintenance/requests/{id}/assign", response_model=dict[str, Any])
async def assign_maintenance_request(
    id: UUID,
    req: MaintenanceRequestAssign,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Assigns an employee to a maintenance request."""
    try:
        async with uow:
            r = await service.assign_maintenance_request(uow, id, req.employee_id)
            return {
                "id": str(r.id),
                "room_id": str(r.room_id),
                "assigned_employee_id": str(r.assigned_employee_id),
                "status": r.status,
                "priority": r.priority,
                "description": r.description,
                "created_at": r.created_at.isoformat(),
                "completed_at": None,
            }
    except (MaintenanceRequestNotFoundError, EmployeeNotFoundError) as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.post("/maintenance/requests/{id}/complete", response_model=dict[str, Any])
async def complete_maintenance_request(
    id: UUID,
    uow: PostgresUnitOfWork = Depends(get_unit_of_work),
) -> dict[str, Any]:
    """Completes a maintenance request."""
    try:
        async with uow:
            r = await service.complete_maintenance_request(uow, id)
            return {
                "id": str(r.id),
                "room_id": str(r.room_id),
                "assigned_employee_id": str(r.assigned_employee_id),
                "status": r.status,
                "priority": r.priority,
                "description": r.description,
                "created_at": r.created_at.isoformat(),
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
            }
    except MaintenanceRequestNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except OpsDomainError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e
