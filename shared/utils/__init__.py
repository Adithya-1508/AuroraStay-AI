import uuid


def generate_uuid(prefix: str = "") -> str:
    """Generates a random UUID string, optionally prepended with a category prefix."""
    raw_id = str(uuid.uuid4())
    return f"{prefix}_{raw_id}" if prefix else raw_id
