import uuid
from collections.abc import Sequence
from datetime import UTC, datetime

from backend.models.housekeeping import HousekeepingTask
from backend.models.maintenance import MaintenanceRequest
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.ops.domain.enums import Priority, TaskStatus
from business.ops.domain.exceptions import (
    EmployeeNotFoundError,
    MaintenanceRequestNotFoundError,
    OpsDomainError,
    RoomNotFoundError,
    TaskNotFoundError,
)
from business.ops.events.publisher import domain_event_publisher
from business.ops.events.schemas import (
    HousekeepingTaskCompleted,
    HousekeepingTaskCreated,
    MaintenanceCompleted,
)


class OperationsService:
    """Core Service managing hotel turnaround logistics and maintenance operations."""

    async def create_housekeeping_task(
        self, uow: AbstractUnitOfWork, room_id: uuid.UUID
    ) -> HousekeepingTask:
        """Creates a pending housekeeping task for a room."""
        # Verify room exists
        room = await uow.rooms.get(str(room_id))
        if not room:
            raise RoomNotFoundError(str(room_id))

        task = HousekeepingTask(
            room_id=room_id,
            status=TaskStatus.PENDING.value,
        )
        await uow.housekeeping.add(task)
        await uow.commit()

        # Publish event
        await domain_event_publisher.publish(
            HousekeepingTaskCreated(
                task_id=task.id,
                room_id=room_id,
                status=task.status,
            )
        )
        return task

    async def assign_housekeeping_task(
        self, uow: AbstractUnitOfWork, task_id: uuid.UUID, employee_id: uuid.UUID
    ) -> HousekeepingTask:
        """Assigns task to employee and marks it as IN_PROGRESS."""
        task = await uow.housekeeping.get(str(task_id))
        if not task:
            raise TaskNotFoundError(str(task_id))

        # Verify employee exists
        employee = await uow.employees.get(str(employee_id))
        if not employee:
            raise EmployeeNotFoundError(str(employee_id))

        task.assigned_employee_id = employee_id
        task.status = TaskStatus.IN_PROGRESS.value
        await uow.housekeeping.update(task)
        await uow.commit()
        return task

    async def complete_housekeeping_task(
        self, uow: AbstractUnitOfWork, task_id: uuid.UUID
    ) -> HousekeepingTask:
        """Marks task as COMPLETED and transitions room status to Clean."""
        task = await uow.housekeeping.get(str(task_id))
        if not task:
            raise TaskNotFoundError(str(task_id))

        if not task.assigned_employee_id:
            raise OpsDomainError("Cannot complete task without an assigned employee.")

        task.status = TaskStatus.COMPLETED.value
        task.completed_at = datetime.now(UTC)
        await uow.housekeeping.update(task)

        # Transition physical room status to Clean
        room = await uow.rooms.get(str(task.room_id))
        if room:
            room.status = "Clean"
            await uow.rooms.update(room)

        await uow.commit()

        # Publish event
        await domain_event_publisher.publish(
            HousekeepingTaskCompleted(
                task_id=task.id,
                room_id=task.room_id,
                assigned_employee_id=task.assigned_employee_id,
            )
        )
        return task

    async def list_housekeeping_tasks(
        self, uow: AbstractUnitOfWork, status: str | None = None
    ) -> Sequence[HousekeepingTask]:
        """Lists housekeeping tasks, optionally filtered by status."""
        tasks = await uow.housekeeping.get_all()
        if status:
            return [t for t in tasks if t.status == status]
        return tasks

    async def create_maintenance_request(
        self,
        uow: AbstractUnitOfWork,
        room_id: uuid.UUID,
        description: str,
        priority: str,
    ) -> MaintenanceRequest:
        """Creates a maintenance request. If priority is URGENT, sets room status to Under Maintenance."""
        # Verify room exists
        room = await uow.rooms.get(str(room_id))
        if not room:
            raise RoomNotFoundError(str(room_id))

        # Validate priority enum
        try:
            p_val = Priority(priority.upper()).value
        except ValueError:
            p_val = Priority.LOW.value

        request = MaintenanceRequest(
            room_id=room_id,
            description=description,
            priority=p_val,
            status=TaskStatus.PENDING.value,
        )
        await uow.maintenance.add(request)

        # Urgent requests transition room immediately to Under Maintenance
        if p_val == Priority.URGENT.value:
            room.status = "Under Maintenance"
            await uow.rooms.update(room)

        await uow.commit()
        return request

    async def assign_maintenance_request(
        self, uow: AbstractUnitOfWork, request_id: uuid.UUID, employee_id: uuid.UUID
    ) -> MaintenanceRequest:
        """Assigns request to employee and marks it as IN_PROGRESS."""
        request = await uow.maintenance.get(str(request_id))
        if not request:
            raise MaintenanceRequestNotFoundError(str(request_id))

        # Verify employee exists
        employee = await uow.employees.get(str(employee_id))
        if not employee:
            raise EmployeeNotFoundError(str(employee_id))

        request.assigned_employee_id = employee_id
        request.status = TaskStatus.IN_PROGRESS.value
        await uow.maintenance.update(request)
        await uow.commit()
        return request

    async def complete_maintenance_request(
        self, uow: AbstractUnitOfWork, request_id: uuid.UUID
    ) -> MaintenanceRequest:
        """Marks request as COMPLETED and transitions room status back to Clean."""
        request = await uow.maintenance.get(str(request_id))
        if not request:
            raise MaintenanceRequestNotFoundError(str(request_id))

        if not request.assigned_employee_id:
            raise OpsDomainError(
                "Cannot complete maintenance request without an assigned employee."
            )

        request.status = TaskStatus.COMPLETED.value
        request.completed_at = datetime.now(UTC)
        await uow.maintenance.update(request)

        # Transition room back to Clean
        room = await uow.rooms.get(str(request.room_id))
        if room:
            room.status = "Clean"
            await uow.rooms.update(room)

        await uow.commit()

        # Publish event
        await domain_event_publisher.publish(
            MaintenanceCompleted(
                request_id=request.id,
                room_id=request.room_id,
                assigned_employee_id=request.assigned_employee_id,
            )
        )
        return request

    async def list_maintenance_requests(
        self, uow: AbstractUnitOfWork, status: str | None = None
    ) -> Sequence[MaintenanceRequest]:
        """Lists maintenance requests, optionally filtered by status."""
        requests = await uow.maintenance.get_all()
        if status:
            return [r for r in requests if r.status == status]
        return requests
