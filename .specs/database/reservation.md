# Database Specification: Reservation

Defines the structure and constraints of the `reservations` table.

## Schema Details

- **Table Name**: `reservations`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `guest_id`: UUID (Foreign Key to `guests.id`), not null
  - `room_category_id`: UUID (Foreign Key to `room_categories.id`), not null
  - `assigned_room_id`: UUID (Foreign Key to `rooms.id`), nullable
  - `check_in_date`: DATE, not null
  - `check_out_date`: DATE, not null
  - `total_cost`: NUMERIC(12, 2), not null
  - `status`: VARCHAR(50), default "Pending", not null (Pending, Confirmed, CheckedIn, CheckedOut, Cancelled)
  - `version`: INTEGER, default 1, not null (optimistic locking)
  - `created_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `updated_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `created_by`: VARCHAR(100), nullable
  - `updated_by`: VARCHAR(100), nullable
  - `is_deleted`: BOOLEAN, default FALSE, not null
  - `deleted_at`: TIMESTAMP WITH TIME ZONE, nullable

## Indexes

- Primary Key unique index on `id`.
- Index on `guest_id` (FK joins optimization).
- Index on `assigned_room_id` (availability tracking).
- Index on `check_in_date, check_out_date` (booking queries).
- Index on `status`.

## Relationships

- Many-to-one with `guests`.
- Many-to-one with `room_categories`.
- Many-to-one with `rooms` (optional).
- One-to-one with `reviews` (optional).
