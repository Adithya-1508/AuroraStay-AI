# Operations API Reference

The Operations Platform routes are mounted under `/api/v1/housekeeping` and `/api/v1/maintenance`.

## Endpoints Catalog

### Housekeeping turnaround
* **GET `/api/v1/housekeeping/tasks`**
  Lists turnaround tasks, optionally filtered by `status_filter` query parameter.
* **POST `/api/v1/housekeeping/tasks`**
  Manually spins up a turnaround task.
  - Body: `HousekeepingTaskCreate`
* **POST `/api/v1/housekeeping/tasks/{id}/assign`**
  Assigns a housekeeper employee to a task.
  - Body: `HousekeepingTaskAssign`
* **POST `/api/v1/housekeeping/tasks/{id}/complete`**
  Completes cleaning and sets Room status to `Clean`.

### Maintenance requests
* **GET `/api/v1/maintenance/requests`**
  Lists all maintenance requests.
* **POST `/api/v1/maintenance/requests`**
  Registers a maintenance repair work order.
  - Body: `MaintenanceRequestCreate`
* **POST `/api/v1/maintenance/requests/{id}/assign`**
  Assigns a technician employee to a request.
  - Body: `MaintenanceRequestAssign`
* **POST `/api/v1/maintenance/requests/{id}/complete`**
  Completes repair work order and sets Room status to `Clean`.
