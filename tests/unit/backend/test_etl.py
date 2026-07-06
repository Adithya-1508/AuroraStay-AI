from collections.abc import AsyncGenerator
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.data_quality import DataQualityEvaluator
from backend.etl import (
    DatabaseLoader,
    IngestionValidator,
    MetadataCatalog,
    PMSDataTransformer,
    PMSMockExtractor,
)
from backend.models.base import Base


@pytest_asyncio.fixture
async def sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    """Sets up an in-memory SQLite database connection and yields a session maker."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_maker() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_full_etl_pipeline_flow(sqlite_session: AsyncSession) -> None:
    # 1. Extraction
    extractor = PMSMockExtractor()
    raw_data = extractor.extract()
    assert len(raw_data) == 2

    # 2. Transformation
    transformer = PMSDataTransformer()
    transformed_data = transformer.transform(raw_data)
    assert len(transformed_data) == 2
    assert transformed_data[0]["guest_email"] == "john.watson@example.com"
    assert transformed_data[0]["check_in"] == date(2026, 7, 10)

    # 3. Validation
    validator = IngestionValidator()
    is_valid, valid_records = validator.validate_pms_records(transformed_data)
    assert is_valid is True
    assert len(valid_records) == 2

    # 4. Ingestion Loading
    loader = DatabaseLoader(sqlite_session)
    loaded_count = await loader.load_pms_records(valid_records)
    assert loaded_count == 2
    await sqlite_session.commit()

    # 5. Metadata Cataloging
    catalog = MetadataCatalog(sqlite_session)
    execution = await catalog.log_execution(
        dataset_name="pms_bookings",
        dataset_version="v1.0.0",
        source="pms_mock_extractor",
        row_counts=loaded_count,
        validation_status="PASSED",
        execution_duration_sec=0.150,
    )
    assert execution.id is not None
    await sqlite_session.commit()

    # 6. Quality Metrics Evaluator
    evaluator = DataQualityEvaluator()
    quality_report = evaluator.evaluate(transformed_data)
    assert quality_report["completeness_score"] == 1.0
    assert quality_report["validity_score"] == 1.0
    assert quality_report["uniqueness_score"] == 1.0
