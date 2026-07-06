# Spec: Data Platform & Databases

- **Status**: Ready
- **Owner**: Data Platform Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define database schema configurations, SQLAlchemy connection pools, transaction limits, Alembic migrations, and ETL pipeline processes.

## 2. Responsibilities
- Manage database connections utilizing async connection pooling.
- Manage transactional bounds (ACID) across business service layers.
- Apply database migrations (using Alembic).
- Load development seed tables (rooms, rates).
- Coordinate daily ETL tasks extracting booking logs, normalizing reviews, and writing aggregates to target directories.

## 3. Dependencies
- **PostgreSQL**: Relational storage engine.
- **SQLAlchemy 2.x (Async)**: ORM mapper and pool manager.
- **Alembic**: Migration framework.
- **MinIO**: CSV seed source and ETL extraction point.

## 4. Public Interfaces
```python
class DatabaseSessionManager:
    def init_pool(self, db_url: str) -> None:
        """Initializes connection engine and async session factory."""
        pass

    async def get_session(self) -> AsyncSession:
        """Dependency returning an active SQLAlchemy session context."""
        pass

class EtlPipeline(ABC):
    @abstractmethod
    async def extract(self) -> RawDataSet:
        pass
    @abstractmethod
    async def transform(self, raw: RawDataSet) -> CleanDataSet:
        pass
    @abstractmethod
    async def load(self, clean: CleanDataSet) -> bool:
        pass
```

## 5. Configuration
- `DB_POOL_SIZE`: Max connection pool size (default: 20).
- `DB_MAX_OVERFLOW`: Max overflow pool size (default: 10).
- `DB_TIMEOUT`: Connection timeout limits (default: 30 seconds).

## 6. Failure Modes
- **Connection Pool Exhaustion**: If the pool runs dry, wait up to 10 seconds. If no connection opens, raise `ConnectionTimeoutError`.
- **ETL Ingestion Failures**: Roll back the active transaction and alert managers via logs if individual ETL rows fail normalization constraints.

## 7. Security Considerations
- Require secure passwords.
- Block SQL injection by enforcing parameterized query binding.

## 8. Testing Strategy
- **Unit Tests**: Mock database engine interfaces to test transaction rollbacks during application use case exceptions.
- **Integration Tests**: Execute real schema upgrades using Alembic migrations against a test PostgreSQL instance.
