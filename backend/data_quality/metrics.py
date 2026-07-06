from typing import Any


class DataQualityEvaluator:
    """Evaluates data quality metrics for dataset records."""

    def evaluate(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        """Runs quality analysis checks on fields, compiling quality scores."""
        total = len(records)
        if total == 0:
            return {
                "completeness_score": 1.0,
                "uniqueness_score": 1.0,
                "validity_score": 1.0,
                "row_count": 0,
            }

        # 1. Calculate Completeness (non-null rates for mandatory columns)
        non_null_email = sum(1 for r in records if r.get("guest_email"))
        non_null_dates = sum(
            1 for r in records if r.get("check_in") and r.get("check_out")
        )

        # Average completeness metric
        completeness = ((non_null_email / total) + (non_null_dates / total)) / 2.0

        # 2. Calculate Uniqueness (duplicate rates on email/booking details)
        unique_emails = len(
            {r.get("guest_email") for r in records if r.get("guest_email")}
        )
        uniqueness = unique_emails / total if total > 0 else 1.0

        # 3. Calculate Validity (passing business rules check rates)
        valid_records = 0
        for r in records:
            check_in = r.get("check_in")
            check_out = r.get("check_out")
            total_cost = r.get("total_cost", 0.0)

            # Rules check
            date_ok = (check_in and check_out and check_in <= check_out) or (
                not check_in or not check_out
            )
            cost_ok = total_cost >= 0.0

            if date_ok and cost_ok:
                valid_records += 1

        validity = valid_records / total

        # Weighted quality score
        overall_score = (completeness + uniqueness + validity) / 3.0

        return {
            "completeness_score": round(completeness, 4),
            "uniqueness_score": round(uniqueness, 4),
            "validity_score": round(validity, 4),
            "overall_quality_score": round(overall_score, 4),
            "row_count": total,
        }


__all__ = ["DataQualityEvaluator"]
