from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Global system configuration settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/hospitality"
    )
    REDIS_URL: str = "redis://localhost:6379/0"
    QDRANT_URL: str = "http://localhost:6333"
    JWT_SECRET: str = "supersecretkeychangeinproduction"  # noqa: S105
    MODEL_PROVIDER: str = "mock"
    DEFAULT_MODEL: str = "mock-model"
    NVIDIA_API_KEY: str = "mock-key"
    OLLAMA_API_URL: str = "http://localhost:11434"
    MLFLOW_URI: str = "http://localhost:5000"
    LOG_LEVEL: str = "INFO"


settings = Settings()
