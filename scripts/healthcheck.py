import socket
import sys


def check_port(host: str, port: int) -> bool:
    """Attempts to establish a TCP connection to the specified port."""
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except (TimeoutError, ConnectionRefusedError):
        return False


def main() -> None:
    services: dict[str, int] = {
        "PostgreSQL (Database)": 5432,
        "Redis (Broker/Cache)": 6379,
        "Qdrant (Vector DB)": 6333,
        "MinIO (Object Store)": 9000,
        "MLflow (Model Registry)": 5000,
    }

    print("Checking local infrastructure services...")
    all_healthy = True
    for name, port in services.items():
        is_up = check_port("localhost", port)
        status = "ONLINE" if is_up else "OFFLINE"
        print(f" - {name} on port {port}: {status}")
        if not is_up:
            all_healthy = False

    if not all_healthy:
        print(
            "\nWarning: Some services are unreachable. "
            "Ensure 'docker compose up -d' is running."
        )
        sys.exit(1)
    else:
        print("\nAll infrastructure services are ONLINE and healthy!")


if __name__ == "__main__":
    main()
