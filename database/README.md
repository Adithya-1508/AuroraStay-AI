# Database Directory

## Purpose
Manages structural migrations, database configuration files, and seed datasets. It handles the relational schema definitions and integration scripts.

## Ownership
- **Owner**: Data Platform Team (Antigravity AI Coding Agent)
- **Primary Domain**: Database Migrations, Seeds, Schema Control

## Key Components
- `migrations/`: Alembic directory storing history of version upgrades.
- `seeds/`: Initial data files (e.g. rooms, room types) used to bootstrap the system.
- `schema/`: Declarative SQL models (mapped through SQLAlchemy).
