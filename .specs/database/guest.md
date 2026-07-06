# Database Specification: Guest

Defines the structure and constraints of the `guests` table.

## Schema Details

- **Table Name**: `guests`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `first_name`: VARCHAR(100), not null
  - `last_name`: VARCHAR(100), not null
  - `email`: VARCHAR(255), unique, index, not null
  - `phone`: VARCHAR(50), nullable
  - `loyalty_tier`: VARCHAR(50), default "Bronze", not null
  - `preferences`: JSONB, nullable (storing temperature and pillow choices)
  - `version`: INTEGER, default 1, not null (optimistic locking)
  - `created_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `updated_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `created_by`: VARCHAR(100), nullable
  - `updated_by`: VARCHAR(100), nullable
  - `is_deleted`: BOOLEAN, default FALSE, not null
  - `deleted_at`: TIMESTAMP WITH TIME ZONE, nullable

## Indexes

- Primary Key unique index on `id`.
- Unique index on `email`.
- Index on `last_name, first_name` for lookup searches.

## Relationships

- One-to-many with `reservations`.
- One-to-many with `reviews`.
- One-to-many with `spa_bookings`.
