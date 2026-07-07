class OpsDomainError(Exception):
    """Base domain exception class for Hotel Operations Platform."""

    pass


class TaskNotFoundError(OpsDomainError):
    """Raised when the requested HousekeepingTask cannot be found."""

    def __init__(self, task_id: str) -> None:
        super().__init__(
            f"Housekeeping task not found.\n"
            f"Task ID: {task_id}\n"
            f"Possible causes: invalid ID, task deleted, database connection issue."
        )


class MaintenanceRequestNotFoundError(OpsDomainError):
    """Raised when the requested MaintenanceRequest cannot be found."""

    def __init__(self, request_id: str) -> None:
        super().__init__(
            f"Maintenance request not found.\n"
            f"Request ID: {request_id}\n"
            f"Possible causes: invalid ID, request deleted, database connection issue."
        )


class EmployeeNotFoundError(OpsDomainError):
    """Raised when the assigned employee cannot be found."""

    def __init__(self, employee_id: str) -> None:
        super().__init__(
            f"Assigned employee not found.\n"
            f"Employee ID: {employee_id}\n"
            f"Possible causes: invalid ID, employee inactive."
        )


class RoomNotFoundError(OpsDomainError):
    """Raised when the target room cannot be found."""

    def __init__(self, room_id: str) -> None:
        super().__init__(
            f"Room not found.\n"
            f"Room ID: {room_id}\n"
            f"Possible causes: invalid ID, room deleted."
        )
