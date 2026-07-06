# Database Specification: Forecast

Defines the structure and constraints of the `forecasts` table.

## Schema Details

- **Table Name**: `forecasts`
- **Columns**:
  - `id`: UUID (Primary Key, unique)
  - `target_date`: DATE, not null
  - `metric_name`: VARCHAR(100), not null (e.g. OccupancyRate, AverageDailyRate, RevPAR)
  - `predicted_value`: NUMERIC(12, 4), not null
  - `confidence_lower`: NUMERIC(12, 4), nullable
  - `confidence_upper`: NUMERIC(12, 4), nullable
  - `forecast_generated_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `created_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `updated_at`: TIMESTAMP WITH TIME ZONE, default NOW(), not null
  - `created_by`: VARCHAR(100), nullable
  - `updated_by`: VARCHAR(100), nullable
  - `is_deleted`: BOOLEAN, default FALSE, not null
  - `deleted_at`: TIMESTAMP WITH TIME ZONE, nullable

## Indexes

- Primary Key unique index on `id`.
- Index on `target_date`.
- Index on `metric_name`.
- Composite Index on `target_date, metric_name`.
