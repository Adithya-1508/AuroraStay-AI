# Database Specification: Room & Room Category

Defines structures and constraints of the `rooms` and `room_categories` tables.

## 1. Room Categories Schema
- **Table Name**: `room_categories`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `name`: VARCHAR(100), unique, not null (Standard, Deluxe, Suite, Executive)
  - `base_price`: NUMERIC(12, 2), not null
  - `created_at` / `updated_at` / audit fields
  - `is_deleted` / `deleted_at`

## 2. Rooms Schema
- **Table Name**: `rooms`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `room_number`: VARCHAR(50), unique, not null
  - `category_id`: UUID (Foreign Key to `room_categories.id`), not null
  - `status`: VARCHAR(50), default "Available", not null (Available, Occupied, Dirty, Maintenance)
  - `version`: INTEGER, default 1, not null (optimistic locking)
  - `created_at` / `updated_at` / audit fields
  - `is_deleted` / `deleted_at`

## Indexes
- Unique index on `room_categories.name`.
- Unique index on `rooms.room_number`.
- Index on `rooms.category_id`.
- Index on `rooms.status` (for availability filters).
