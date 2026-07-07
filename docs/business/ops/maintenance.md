# Maintenance & Repair Management

The maintenance module tracks facility repair work orders.

## Priorities and Status Overrides

HOP supports three priority tiers:
1. **LOW / MEDIUM**: Standard repair logs; target Room status remains unaffected during task assignment.
2. **URGENT**: Immediate critical repair logs; this priority **immediately sets the target Room status to `Under Maintenance`** upon request creation to prevent room booking collisions.

Upon task completion (`complete_maintenance_request`), the physical Room status transitions back to `Clean`.

## Usage Example

```python
from business.ops.services.operations import OperationsService

service = OperationsService()

# Create urgent repair request
req = await service.create_maintenance_request(
    uow, room_id, "Burst pipe", "URGENT"
)
# Room is now "Under Maintenance"

# Technician completes repair
await service.complete_maintenance_request(uow, req.id)
# Room is now "Clean"
```
