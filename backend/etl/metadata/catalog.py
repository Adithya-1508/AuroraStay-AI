from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.etl import ETLExecution


class MetadataCatalog:
    """Metadata Catalog logger recording runs inside etl_executions table."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def log_execution(
        self,
        dataset_name: str,
        dataset_version: str,
        source: str,
        row_counts: int,
        validation_status: str,
        execution_duration_sec: float,
        error_report: dict[str, Any] | None = None,
    ) -> ETLExecution:
        """Saves pipeline runs metadata parameters."""
        execution = ETLExecution(
            dataset_name=dataset_name,
            dataset_version=dataset_version,
            source=source,
            timestamp=datetime.now(UTC),
            row_counts=row_counts,
            validation_status=validation_status,
            execution_duration_sec=execution_duration_sec,
            error_report=error_report,
        )
        self.session.add(execution)
        await self.session.flush()
        return execution


__all__ = ["MetadataCatalog"]
