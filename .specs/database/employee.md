# Database Specification: Employee

Defines the structure and constraints of the `employees` table.

## Schema Details

- **Table Name**: `employees`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `first_name`: VARCHAR(100), not null
  - `last_name`: VARCHAR(100), not null
  - `email`: VARCHAR(255), unique, index, not null
  - `role`: VARCHAR(100), not null (e.g. Housekeeper, FrontDesk, Manager)
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
- Index on `role`.
