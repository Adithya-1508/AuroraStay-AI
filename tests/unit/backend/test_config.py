from backend.core.settings import settings


def test_settings_load() -> None:
    assert settings.DATABASE_URL is not None
    assert settings.REDIS_URL is not None
    assert settings.QDRANT_URL is not None
    assert settings.JWT_SECRET is not None
    assert settings.MODEL_PROVIDER == "mock"
