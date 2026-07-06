# Guest Profiles & CRM Integration

The guest profiles system is the source of truth for all guest metadata, CRM flags, and loyalty states.

## Domain Model

### Guest Entities
* **id**: Unique identifier (UUID).
* **first_name / last_name**: Personal details.
* **email**: Unique, lowercased, and sanitized index email.
* **phone**: Formatted contact string.
* **loyalty_tier**: Loyalty level of the guest:
  - `Bronze` (default)
  - `Silver`
  - `Gold`
  - `Platinum`
  - `VIP`
* **preferences**: Dynamic JSONB schema storing learned guest characteristics.

## Domain Events

The service publishes events asynchronously when profile attributes change:

1. **GuestProfileUpdated**: Fired when fields such as first name, phone, or loyalty status change.
2. **PreferenceChanged**: Published when pillow, room, or dining constraints are learned or modified.

## Usage Example

```python
from business.guest.services.profile import GuestProfileService
from business.guest.domain.value_objects import ProfileDetails

service = GuestProfileService(uow)

# Create profile
guest = await service.create_profile(
    ProfileDetails(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="+1234567890"
    ),
    loyalty_tier="Gold"
)

# Update profile
await service.update_profile(guest.id, {"first_name": "Janet"})
```
