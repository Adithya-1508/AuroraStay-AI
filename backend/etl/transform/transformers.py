import re
from datetime import date, datetime
from typing import Any


def clean_string(val: Any) -> str:
    """Strips whitespace and returns a clean string representation."""
    if val is None:
        return ""
    return str(val).strip()


def clean_email(val: Any) -> str:
    """Lowercases and cleans contact email strings."""
    return clean_string(val).lower()


def clean_phone(val: Any) -> str | None:
    """Normalizes phone numbers to standard structures."""
    cleaned = clean_string(val)
    if not cleaned:
        return None
    # Basic normalization: strip non-digits or keep leading '+' symbol
    has_plus = cleaned.startswith("+")
    digits = re.sub(r"\D", "", cleaned)
    if has_plus:
        return f"+{digits}"
    return digits


def clean_date(val: Any) -> date | None:
    """Parses date representations into python date objects."""
    if isinstance(val, date):
        return val
    if isinstance(val, datetime):
        return val.date()
    cleaned = clean_string(val)
    if not cleaned:
        return None
    try:
        return datetime.strptime(cleaned, "%Y-%m-%d").date()
    except ValueError:
        try:
            return datetime.fromisoformat(cleaned).date()
        except ValueError:
            return None


def clean_decimal(val: Any) -> float:
    """Parses floating decimal values from currency or metric fields."""
    if val is None:
        return 0.0
    try:
        return float(val)
    except ValueError:
        return 0.0


class PMSDataTransformer:
    """Transformer mapping raw PMS ingestion rows to cleaned schemas."""

    def transform(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Maps row dictionaries through cleaning pipelines."""
        transformed = []
        for r in records:
            guest_email = clean_email(r.get("guest_email"))
            first_name = clean_string(r.get("first_name"))
            last_name = clean_string(r.get("last_name"))
            phone = clean_phone(r.get("phone"))
            room_number = clean_string(r.get("room_number"))
            room_category = clean_string(r.get("room_category"))
            check_in = clean_date(r.get("check_in"))
            check_out = clean_date(r.get("check_out"))
            total_cost = clean_decimal(r.get("total_cost"))
            status = clean_string(r.get("status") or "Confirmed")

            transformed.append(
                {
                    "guest_email": guest_email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "room_number": room_number,
                    "room_category": room_category,
                    "check_in": check_in,
                    "check_out": check_out,
                    "total_cost": total_cost,
                    "status": status,
                }
            )
        return transformed


__all__ = [
    "clean_string",
    "clean_email",
    "clean_phone",
    "clean_date",
    "clean_decimal",
    "PMSDataTransformer",
]
