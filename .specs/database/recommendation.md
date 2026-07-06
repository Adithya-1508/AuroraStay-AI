# Database Specification: Recommendation

Defines the structure and constraints of the `recommendations` table.

## Schema Details

- **Table Name**: `recommendations`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `guest_id`: UUID (Foreign Key to `guests.id`), not null
  - `item_type`: VARCHAR(100), not null (e.g. SpaTreatment, RestaurantReservation, RoomUpgrade)
  - `item_reference_id`: UUID, nullable (references appropriate table)
  - `score`: NUMERIC(5, 4), not null (e.g. 0.9856)
  - `is_accepted`: BOOLEAN, default FALSE, not null
  - `generated_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `created_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `updated_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `created_by`: VARCHAR(100), nullable
  - `updated_by`: VARCHAR(100), nullable
  - `is_deleted`: BOOLEAN, default FALSE, not null
  - `deleted_at`: TIMESTAMP WITH TIME ZONE, nullable

## Indexes

- Primary Key unique index on `id`.
- Index on `guest_id`.
- Index on `item_type`.
- Index on `is_accepted`.
