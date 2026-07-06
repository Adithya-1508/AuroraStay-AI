import re
from typing import Any


class IngestionValidator:
    """Validator executing checks against transformed dataset row collections."""

    def __init__(self) -> None:
        self.errors: list[dict[str, Any]] = []

    def validate_pms_records(
        self, records: list[dict[str, Any]]
    ) -> tuple[bool, list[dict[str, Any]]]:
        """Validates transformed PMS bookings, compiling a detailed error report."""
        self.errors = []
        valid_records = []

        for idx, r in enumerate(records):
            row_errors = []
            email = r.get("guest_email", "")
            first_name = r.get("first_name", "")
            last_name = r.get("last_name", "")
            check_in = r.get("check_in")
            check_out = r.get("check_out")
            total_cost = r.get("total_cost", 0.0)

            # 1. Null check on mandatory columns
            if not email:
                row_errors.append("guest_email is missing")
            if not first_name:
                row_errors.append("first_name is missing")
            if not last_name:
                row_errors.append("last_name is missing")
            if not check_in:
                row_errors.append("check_in date is missing")
            if not check_out:
                row_errors.append("check_out date is missing")

            # 2. Email format validation
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                row_errors.append(f"invalid email format: '{email}'")

            # 3. Date ordering constraints
            if check_in and check_out and check_out < check_in:
                row_errors.append(
                    f"check_out date ({check_out}) cannot precede check_in ({check_in})"
                )

            # 4. Total cost bounds checks
            if total_cost < 0.0:
                row_errors.append(f"total_cost ({total_cost}) cannot be negative")

            # Logging errors
            if row_errors:
                self.errors.append(
                    {
                        "row_index": idx,
                        "guest_email": email,
                        "reasons": row_errors,
                    }
                )
            else:
                valid_records.append(r)

        is_valid = len(self.errors) == 0
        return is_valid, valid_records


__all__ = ["IngestionValidator"]
