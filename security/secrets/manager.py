import os


class SecretsManager:
    """Manages secure injection, rotation, and retrieval of credentials."""

    @staticmethod
    def get_secret(key: str, default: str | None = None) -> str | None:
        """Retrieves config secrets from the environment variables safely."""
        return os.environ.get(key, default)

    @staticmethod
    def mask_secret_log(secret_value: str) -> str:
        """Masks sensitive token values for telemetry logs."""
        if len(secret_value) <= 8:
            return "********"
        return f"{secret_value[:4]}...{secret_value[-4:]}"
