# Data Platform: Database Migrations

This document details the Alembic migrations structure, workflows, and configuration environments.

## Operations Flow

1. **Scaffold a Migration**:
   - Write/edit model classes under `backend/models/`.
   - Run Alembic autogenerate command:
     ```bash
     .venv/Scripts/alembic revision --autogenerate -m "Add table name"
     ```
2. **Apply Migrations**:
   - Execute upgrade head command:
     ```bash
     .venv/Scripts/alembic upgrade head
     ```
3. **Rollback Migrations**:
   - Execute downgrade revision command:
     ```bash
     .venv/Scripts/alembic downgrade -1
     ```

## Code Configurations

- `env.py`: Connection parameters are read dynamically from `settings.DATABASE_URL` (with asyncpg dialect mappings).
- Metadata targets: Associated with `Base.metadata` to support autogeneration workflows.
