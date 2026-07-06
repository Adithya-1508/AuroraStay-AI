import shutil
from pathlib import Path


def bootstrap() -> None:
    """Bootstraps directories and environment configurations for HospitalityAI."""
    root = Path(__file__).parent.parent.resolve()
    print(f"Bootstrapping HospitalityAI at {root}...")

    # Copy env if missing
    env_file = root / ".env"
    env_example = root / ".env.example"
    if not env_file.exists() and env_example.exists():
        print("Creating .env from .env.example...")
        shutil.copy(env_example, env_file)
    elif env_file.exists():
        print(".env file already exists.")

    print("\nBootstrap complete! Ready for development.")


if __name__ == "__main__":
    bootstrap()
