import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.employee import Employee
from backend.models.room import Room, RoomCategory
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.ops.domain.enums import Priority, TaskStatus
from business.ops.domain.exceptions import (
    EmployeeNotFoundError,
    MaintenanceRequestNotFoundError,
    OpsDomainError,
    RoomNotFoundError,
    TaskNotFoundError,
)
from business.ops.services.operations import OperationsService
from business.reservation.events.publisher import (
    domain_event_publisher as res_publisher,
)
from business.reservation.events.schemas import ReservationCheckedOut


@pytest.mark.asyncio
async def test_housekeeping_task_lifecycle(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork()
    service = OperationsService()

    # Setup room category, room, and employee
    async with uow:
        cat = RoomCategory(name="Deluxe Suite", base_price=150.0)
        await uow.room_categories.add(cat)
        await uow.commit()

        room = Room(room_number="401", category_id=cat.id, status="Dirty")
        await uow.rooms.add(room)

        emp = Employee(
            first_name="John",
            last_name="Doe",
            email="john.doe@hotel.com",
            role="Housekeeper",
        )
        await uow.employees.add(emp)
        await uow.commit()

        room_id = room.id
        employee_id = emp.id

    # 1. Create task
    task = await service.create_housekeeping_task(uow, room_id)
    assert task.room_id == room_id
    assert task.status == TaskStatus.PENDING.value
    assert task.assigned_employee_id is None

    # Invalid room creation error
    with pytest.raises(RoomNotFoundError):
        await service.create_housekeeping_task(uow, uuid.uuid4())

    # 2. Assign task
    task = await service.assign_housekeeping_task(uow, task.id, employee_id)
    assert task.assigned_employee_id == employee_id
    assert task.status == TaskStatus.IN_PROGRESS.value

    # Assign task - task not found
    with pytest.raises(TaskNotFoundError):
        await service.assign_housekeeping_task(uow, uuid.uuid4(), employee_id)

    # Assign task - employee not found
    with pytest.raises(EmployeeNotFoundError):
        await service.assign_housekeeping_task(uow, task.id, uuid.uuid4())

    # 3. Complete task (unassigned task failure)
    unassigned_task = await service.create_housekeeping_task(uow, room_id)
    with pytest.raises(OpsDomainError):
        await service.complete_housekeeping_task(uow, unassigned_task.id)

    # Complete task success
    completed_task = await service.complete_housekeeping_task(uow, task.id)
    assert completed_task.status == TaskStatus.COMPLETED.value
    assert completed_task.completed_at is not None

    async with uow:
        updated_room = await uow.rooms.get(str(room_id))
        assert updated_room is not None
        assert updated_room.status == "Clean"

    # Complete task - task not found
    with pytest.raises(TaskNotFoundError):
        await service.complete_housekeeping_task(uow, uuid.uuid4())

    # 4. List tasks
    all_tasks = await service.list_housekeeping_tasks(uow)
    assert len(all_tasks) >= 2
    pending_tasks = await service.list_housekeeping_tasks(uow, TaskStatus.PENDING.value)
    assert len(pending_tasks) == 1


@pytest.mark.asyncio
async def test_maintenance_request_lifecycle(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork()
    service = OperationsService()

    # Setup room category, room, and employee
    async with uow:
        cat = RoomCategory(name="Standard", base_price=100.0)
        await uow.room_categories.add(cat)
        await uow.commit()

        room = Room(room_number="402", category_id=cat.id, status="Clean")
        await uow.rooms.add(room)

        emp = Employee(
            first_name="Bob",
            last_name="Builder",
            email="bob@hotel.com",
            role="Technician",
        )
        await uow.employees.add(emp)
        await uow.commit()

        room_id = room.id
        employee_id = emp.id

    # 1. Create maintenance request (standard priority)
    req = await service.create_maintenance_request(
        uow, room_id, "Leaking shower head", "MEDIUM"
    )
    assert req.room_id == room_id
    assert req.priority == Priority.MEDIUM.value
    assert req.status == TaskStatus.PENDING.value

    # Check room status remains Clean
    async with uow:
        db_room = await uow.rooms.get(str(room_id))
        assert db_room is not None
        assert db_room.status == "Clean"

    # Room not found exception
    with pytest.raises(RoomNotFoundError):
        await service.create_maintenance_request(
            uow, uuid.uuid4(), "Leaking shower", "LOW"
        )

    # 2. Assign request
    req = await service.assign_maintenance_request(uow, req.id, employee_id)
    assert req.assigned_employee_id == employee_id
    assert req.status == TaskStatus.IN_PROGRESS.value

    # Assign request - request not found
    with pytest.raises(MaintenanceRequestNotFoundError):
        await service.assign_maintenance_request(uow, uuid.uuid4(), employee_id)

    # Assign request - employee not found
    with pytest.raises(EmployeeNotFoundError):
        await service.assign_maintenance_request(uow, req.id, uuid.uuid4())

    # 3. Complete request (unassigned request failure)
    unassigned_req = await service.create_maintenance_request(
        uow, room_id, "Light bulb broken", "LOW"
    )
    with pytest.raises(OpsDomainError):
        await service.complete_maintenance_request(uow, unassigned_req.id)

    # Complete request success
    completed_req = await service.complete_maintenance_request(uow, req.id)
    assert completed_req.status == TaskStatus.COMPLETED.value
    assert completed_req.completed_at is not None

    # Complete request - not found exception
    with pytest.raises(MaintenanceRequestNotFoundError):
        await service.complete_maintenance_request(uow, uuid.uuid4())

    # 4. List requests
    all_reqs = await service.list_maintenance_requests(uow)
    assert len(all_reqs) >= 2
    pending_reqs = await service.list_maintenance_requests(
        uow, TaskStatus.PENDING.value
    )
    assert len(pending_reqs) >= 1

    # 5. Create urgent request (sets room Under Maintenance)
    urgent_req = await service.create_maintenance_request(
        uow, room_id, "Broken window", "URGENT"
    )
    assert urgent_req.priority == Priority.URGENT.value

    # 6. Create request with invalid priority (should fallback to LOW)
    fallback_req = await service.create_maintenance_request(
        uow, room_id, "Flickering light", "INVALID"
    )
    assert fallback_req.priority == Priority.LOW.value

    async with uow:
        db_room = await uow.rooms.get(str(room_id))
        assert db_room is not None
        assert db_room.status == "Under Maintenance"


@pytest.mark.asyncio
async def test_checkout_housekeeping_workflow(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork()
    service = OperationsService()

    # Setup room category and room
    async with uow:
        cat = RoomCategory(name="Double Room", base_price=120.0)
        await uow.room_categories.add(cat)
        await uow.commit()

        room = Room(room_number="403", category_id=cat.id, status="Dirty")
        await uow.rooms.add(room)
        await uow.commit()

        room_id = room.id

    # Publish ReservationCheckedOut event
    event = ReservationCheckedOut(reservation_id=uuid.uuid4(), room_id=room_id)
    await res_publisher.publish(event)

    # Verify task auto-created
    tasks = await service.list_housekeeping_tasks(uow, TaskStatus.PENDING.value)
    task_match = [t for t in tasks if t.room_id == room_id]
    assert len(task_match) == 1
    assert task_match[0].status == TaskStatus.PENDING.value


@pytest.mark.asyncio
async def test_checkout_housekeeping_workflow_error(db_session: AsyncSession) -> None:
    # Trigger exception path in event consumer by passing invalid room_id
    from business.ops.workflows.event_consumers import handle_checkout_event

    event = ReservationCheckedOut(reservation_id=uuid.uuid4(), room_id=uuid.uuid4())
    await handle_checkout_event(event)
    # The handler logs and suppresses the error, allowing test to complete
