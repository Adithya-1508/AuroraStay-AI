# Database Specification: Review

Defines the structure and constraints of the `reviews` table.

## Schema Details

- **Table Name**: `reviews`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `reservation_id`: UUID (Foreign Key to `reservations.id`), unique, nullable
  - `guest_id`: UUID (Foreign Key to `guests.id`), not null
  - `score`: INTEGER, not null (check range 1 to 5)
  - `content`: TEXT, nullable
  - `submitted_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `sentiment`: VARCHAR(50), nullable
  - `version`: INTEGER, default 1, not null
  - `created_at` / `updated_at` / audit fields
  - `is_deleted` / `deleted_at`

## Indexes

- Unique index on `reservation_id`.
- Index on `guest_id`.
- Index on `score`.
- Index on `sentiment`.
