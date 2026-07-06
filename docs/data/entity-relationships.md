# Data Platform: Entity Relationships

This document details the relational entity maps, foreign key paths, and referential structures.

## Relationships Map

```
  [guests] 1 ──── * [reservations] * ──── 1 [rooms]
     │                    │                     │
     │ 1                  │ 1                   │ 1
     ▼                    ▼                     ▼
  [reviews] 1 ──────── 1 [reviews]        [room_categories]
     ▲
     │
  [spa_bookings] * ──── 1 [spas]
```

## Joins Descriptions

1. **Guest to Reservation**:
   - `guests.id` maps to many `reservations.guest_id`.
   - Cascade delete: When a guest record is deleted, all their reservation records are deleted (or soft-deleted).
2. **Room Category to Room**:
   - `room_categories.id` maps to many `rooms.category_id`.
3. **Room to Reservation**:
   - `rooms.id` maps to many `reservations.assigned_room_id`.
4. **Reservation to Review**:
   - `reservations.id` maps to one `reviews.reservation_id`.
5. **Guest to Review**:
   - `guests.id` maps to many `reviews.guest_id`.
6. **Guest to Spa Booking**:
   - `guests.id` maps to many `spa_bookings.guest_id`.
7. **Spa to Spa Booking**:
   - `spas.id` maps to many `spa_bookings.spa_id`.
