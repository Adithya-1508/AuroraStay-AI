from enum import StrEnum


class TaskStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Priority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    URGENT = "URGENT"
