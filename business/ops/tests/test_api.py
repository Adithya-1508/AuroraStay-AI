import uuid

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.employee import Employee
from backend.models.room import Room, RoomCategory
from backend.repositories.unit_of_work import PostgresUnitOfWork
from business.ops.api.routes import (
    HousekeepingTaskAssign,
    HousekeepingTaskCreate,
    MaintenanceRequestAssign,
    MaintenanceRequestCreate,
    assign_housekeeping_task,
    assign_maintenance_request,
    complete_housekeeping_task,
    complete_maintenance_request,
    create_housekeeping_task,
    create_maintenance_request,
    get_unit_of_work,
    list_housekeeping_tasks,
    list_maintenance_requests,
)


@pytest.mark.asyncio
async def test_get_unit_of_work_coverage() -> None:
    # Exercise the get_unit_of_work factory function
    uow = get_unit_of_work()
    assert isinstance(uow, PostgresUnitOfWork)


@pytest.mark.asyncio
async def test_housekeeping_routes_direct(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore

    async with uow:
        cat = RoomCategory(name="Ops API Category", base_price=110.0)
        await uow.room_categories.add(cat)
        await uow.commit()

        room = Room(room_number="601", category_id=cat.id, status="Dirty")
        await uow.rooms.add(room)

        emp = Employee(
            first_name="Housekeeper",
            last_name="Direct",
            email="hk_direct@hotel.com",
            role="Housekeeper",
        )
        await uow.employees.add(emp)
        await uow.commit()

        room_id = room.id
        employee_id = emp.id

    # 1. Create task
    req_create = HousekeepingTaskCreate(room_id=room_id)
    t = await create_housekeeping_task(req_create, uow)
    assert t["room_id"] == str(room_id)
    assert t["status"] == "PENDING"
    task_id = uuid.UUID(t["id"])

    # Create task room not found
    with pytest.raises(HTTPException) as exc:
        await create_housekeeping_task(
            HousekeepingTaskCreate(room_id=uuid.uuid4()), uow
        )
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    # 2. List tasks
    tasks = await list_housekeeping_tasks(None, uow)
    assert len(tasks) >= 1

    tasks_filtered = await list_housekeeping_tasks("PENDING", uow)
    assert len(tasks_filtered) >= 1

    # 3. Assign task
    req_assign = HousekeepingTaskAssign(employee_id=employee_id)
    t_assigned = await assign_housekeeping_task(task_id, req_assign, uow)
    assert t_assigned["assigned_employee_id"] == str(employee_id)
    assert t_assigned["status"] == "IN_PROGRESS"

    # Assign task task not found
    with pytest.raises(HTTPException) as exc:
        await assign_housekeeping_task(uuid.uuid4(), req_assign, uow)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    # 4. Complete task (unassigned complete error)
    t_unassigned = await create_housekeeping_task(
        HousekeepingTaskCreate(room_id=room_id), uow
    )
    unassigned_task_id = uuid.UUID(t_unassigned["id"])
    with pytest.raises(HTTPException) as exc:
        await complete_housekeeping_task(unassigned_task_id, uow)
    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Complete task success
    t_completed = await complete_housekeeping_task(task_id, uow)
    assert t_completed["status"] == "COMPLETED"
    assert t_completed["completed_at"] is not None

    # Complete task not found
    with pytest.raises(HTTPException) as exc:
        await complete_housekeeping_task(uuid.uuid4(), uow)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_maintenance_routes_direct(db_session: AsyncSession) -> None:
    uow = PostgresUnitOfWork(session_factory=lambda: db_session)  # type: ignore

    async with uow:
        cat = RoomCategory(name="Ops API Category 2", base_price=120.0)
        await uow.room_categories.add(cat)
        await uow.commit()

        room = Room(room_number="602", category_id=cat.id, status="Clean")
        await uow.rooms.add(room)

        emp = Employee(
            first_name="Tech",
            last_name="Direct",
            email="tech_direct@hotel.com",
            role="Technician",
        )
        await uow.employees.add(emp)
        await uow.commit()

        room_id = room.id
        employee_id = emp.id

    # 1. Create request
    req_create = MaintenanceRequestCreate(
        room_id=room_id, description="Broken light", priority="LOW"
    )
    r = await create_maintenance_request(req_create, uow)
    assert r["room_id"] == str(room_id)
    assert r["status"] == "PENDING"
    req_id = uuid.UUID(r["id"])

    # Create request room not found
    with pytest.raises(HTTPException) as exc:
        await create_maintenance_request(
            MaintenanceRequestCreate(room_id=uuid.uuid4(), description="Leak"), uow
        )
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    # 2. List requests
    reqs = await list_maintenance_requests(None, uow)
    assert len(reqs) >= 1

    reqs_filtered = await list_maintenance_requests("PENDING", uow)
    assert len(reqs_filtered) >= 1

    # 3. Assign request
    req_assign = MaintenanceRequestAssign(employee_id=employee_id)
    r_assigned = await assign_maintenance_request(req_id, req_assign, uow)
    assert r_assigned["assigned_employee_id"] == str(employee_id)
    assert r_assigned["status"] == "IN_PROGRESS"

    # Assign request request not found
    with pytest.raises(HTTPException) as exc:
        await assign_maintenance_request(uuid.uuid4(), req_assign, uow)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND

    # 4. Complete request (unassigned request complete error)
    r_unassigned = await create_maintenance_request(
        MaintenanceRequestCreate(room_id=room_id, description="Broken door lock"), uow
    )
    unassigned_req_id = uuid.UUID(r_unassigned["id"])
    with pytest.raises(HTTPException) as exc:
        await complete_maintenance_request(unassigned_req_id, uow)
    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Complete request success
    r_completed = await complete_maintenance_request(req_id, uow)
    assert r_completed["status"] == "COMPLETED"
    assert r_completed["completed_at"] is not None

    # Complete request not found
    with pytest.raises(HTTPException) as exc:
        await complete_maintenance_request(uuid.uuid4(), uow)
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
