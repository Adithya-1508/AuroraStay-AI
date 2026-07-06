# Data Platform: Database Schema

This document details the relational database table layouts and schemas defined for the HospitalityAI platform.

## 1. Guests Table (`guests`)
Stores guest CRM profiles and JSONB preference properties.
- `id` (UUID, Primary Key)
- `first_name` (VARCHAR(100), NOT NULL)
- `last_name` (VARCHAR(100), NOT NULL)
- `email` (VARCHAR(255), UNIQUE, INDEX, NOT NULL)
- `phone` (VARCHAR(50), NULLABLE)
- `loyalty_tier` (VARCHAR(50), NOT NULL, default "Bronze")
- `preferences` (JSONB, NULLABLE)
- `version` (INTEGER, NOT NULL, default 1) - Optimistic locking field.
- `created_at`, `updated_at`, `created_by`, `updated_by` (Standard audit fields)
- `is_deleted`, `deleted_at` (Standard soft delete fields)

## 2. Reservations Table (`reservations`)
Stores stay check-in and check-out arrangements.
- `id` (UUID, Primary Key)
- `guest_id` (UUID, Foreign Key to `guests.id`, NOT NULL)
- `room_category_id` (UUID, Foreign Key to `room_categories.id`, NOT NULL)
- `assigned_room_id` (UUID, Foreign Key to `rooms.id`, NULLABLE)
- `check_in_date` (DATE, NOT NULL)
- `check_out_date` (DATE, NOT NULL)
- `total_cost` (NUMERIC(12, 2), NOT NULL)
- `status` (VARCHAR(50), NOT NULL, default "Pending")
- `version` (INTEGER, NOT NULL, default 1)
- Audit & Soft delete fields

## 3. Rooms Table (`rooms`)
Represents hotel building rooms tracking.
- `id` (UUID, Primary Key)
- `room_number` (VARCHAR(50), UNIQUE, INDEX, NOT NULL)
- `category_id` (UUID, Foreign Key to `room_categories.id`, NOT NULL)
- `status` (VARCHAR(50), NOT NULL, default "Available")
- `version` (INTEGER, NOT NULL, default 1)
- Audit & Soft delete fields

## 4. Room Categories Table (`room_categories`)
Represents room category tiers and base pricing.
- `id` (UUID, Primary Key)
- `name` (VARCHAR(100), UNIQUE, NOT NULL)
- `base_price` (NUMERIC(12, 2), NOT NULL)
- Audit & Soft delete fields

## 5. Reviews Table (`reviews`)
Keeps guest feedback and sentiments.
- `id` (UUID, Primary Key)
- `reservation_id` (UUID, Foreign Key to `reservations.id`, UNIQUE, NULLABLE)
- `guest_id` (UUID, Foreign Key to `guests.id`, NOT NULL)
- `score` (INTEGER, NOT NULL)
- `content` (TEXT, NULLABLE)
- `submitted_at` (TIMESTAMP WITH TIME ZONE, NOT NULL)
- `sentiment` (VARCHAR(50), NULLABLE)
- `version` (INTEGER, NOT NULL, default 1)
- Audit & Soft delete fields

## 6. Employees Table (`employees`)
Keeps employee logs and operations roles.
- `id` (UUID, Primary Key)
- `first_name` (VARCHAR(100), NOT NULL)
- `last_name` (VARCHAR(100), NOT NULL)
- `email` (VARCHAR(255), UNIQUE, INDEX, NOT NULL)
- `role` (VARCHAR(100), NOT NULL)
- `version` (INTEGER, NOT NULL, default 1)
- Audit & Soft delete fields

## 7. Spas Table (`spas`)
Keeps spa services logs.
- `id` (UUID, Primary Key)
- `name` (VARCHAR(100), NOT NULL)
- `treatment_type` (VARCHAR(100), NOT NULL)
- `duration_minutes` (INTEGER, NOT NULL)
- Audit & Soft delete fields

## 8. Spa Bookings Table (`spa_bookings`)
Keeps spa sessions logs.
- `id` (UUID, Primary Key)
- `guest_id` (UUID, Foreign Key to `guests.id`, NOT NULL)
- `spa_id` (UUID, Foreign Key to `spas.id`, NOT NULL)
- `booking_time` (TIMESTAMP WITH TIME ZONE, NOT NULL)
- `status` (VARCHAR(50), NOT NULL, default "Confirmed")
- Audit & Soft delete fields

## 9. Conversations Table (`conversations`)
Tracks guest communications channels.
- `id` (UUID, Primary Key)
- `guest_id` (UUID, Foreign Key to `guests.id`, NULLABLE)
- `channel` (VARCHAR(50), NOT NULL)
- `messages` (JSONB, NULLABLE)
- `version` (INTEGER, NOT NULL, default 1)
- Audit & Soft delete fields

## 10. Recommendations Table (`recommendations`)
Tracks offering recommendations.
- `id` (UUID, Primary Key)
- `guest_id` (UUID, Foreign Key to `guests.id`, NOT NULL)
- `item_type` (VARCHAR(100), NOT NULL)
- `item_reference_id` (UUID, NULLABLE)
- `score` (NUMERIC(5, 4), NOT NULL)
- `is_accepted` (BOOLEAN, NOT NULL, default FALSE)
- `generated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL)
- Audit & Soft delete fields

## 11. Forecasts Table (`forecasts`)
Tracks metric forecasts.
- `id` (UUID, Primary Key)
- `target_date` (DATE, NOT NULL)
- `metric_name` (VARCHAR(100), NOT NULL)
- `predicted_value` (NUMERIC(12, 4), NOT NULL)
- `confidence_lower` (NUMERIC(12, 4), NULLABLE)
- `confidence_upper` (NUMERIC(12, 4), NULLABLE)
- `forecast_generated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL)
- Audit & Soft delete fields

## 12. Knowledge Documents Table (`knowledge_documents`)
Tracks knowledge bases.
- `id` (UUID, Primary Key)
- `title` (VARCHAR(255), NOT NULL)
- `content` (TEXT, NOT NULL)
- `category` (VARCHAR(100), NOT NULL)
- Audit & Soft delete fields

## 13. Notifications Table (`notifications`)
Tracks system notifications.
- `id` (UUID, Primary Key)
- `guest_id` (UUID, Foreign Key to `guests.id`, NULLABLE)
- `employee_id` (UUID, Foreign Key to `employees.id`, NULLABLE)
- `title` (VARCHAR(255), NOT NULL)
- `body` (TEXT, NOT NULL)
- `is_read` (BOOLEAN, NOT NULL, default FALSE)
- `version` (INTEGER, NOT NULL, default 1)
- Audit & Soft delete fields

## 14. ETL Ingestion Log Table (`etl_executions`)
Logs pipeline execution runs.
- `id` (UUID, Primary Key)
- `dataset_name` (VARCHAR(100), NOT NULL)
- `dataset_version` (VARCHAR(50), NOT NULL)
- `source` (VARCHAR(255), NOT NULL)
- `timestamp` (TIMESTAMP WITH TIME ZONE, NOT NULL)
- `row_counts` (INTEGER, NOT NULL)
- `validation_status` (VARCHAR(50), NOT NULL)
- `execution_duration_sec` (NUMERIC(10, 3), NOT NULL)
- `error_report` (JSONB, NULLABLE)
