# Housekeeping Turnaround Workflow

The housekeeping module automates room cleaning turnaround assignments.

## Turnaround States
- **PENDING**: The room is dirty and queued for assignment.
- **IN_PROGRESS**: A housekeeper has been assigned to clean the room.
- **COMPLETED**: The cleaning is finished, updating the physical Room status to `Clean`.

## Checkout Hook Integration
HOP subscribes to the `ReservationCheckedOut` domain event. Upon reception:
1. It validates the room associated with the checkout.
2. It automatically creates a new `HousekeepingTask` with `PENDING` status.
3. It posts the task to the Housekeeping queue.

## Usage example

```python
from business.ops.services.operations import OperationsService

service = OperationsService()

# Assign housekeeper
await service.assign_housekeeping_task(uow, task_id, employee_id)

# Complete turnaround
await service.complete_housekeeping_task(uow, task_id)
```
