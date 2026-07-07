from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class OpsBaseEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1


class HousekeepingTaskCreated(OpsBaseEvent):
    task_id: UUID
    room_id: UUID
    status: str


class HousekeepingTaskCompleted(OpsBaseEvent):
    task_id: UUID
    room_id: UUID
    assigned_employee_id: UUID | None


class MaintenanceCompleted(OpsBaseEvent):
    request_id: UUID
    room_id: UUID
    assigned_employee_id: UUID | None
