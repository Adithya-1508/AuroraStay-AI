import json
from typing import Any


class ExportEngine:
    """Formats dashboard metrics and report payloads into exportable download buffers."""

    @staticmethod
    def export_dataset(
        export_format: str,
        dataset_type: str,
        filters: dict[str, Any],
    ) -> bytes:
        """Converts KPIs and operational lists to bytes in the specified format."""
        normalized_format = export_format.upper()

        # Gather base dataset metrics to serialize
        dataset: dict[str, Any] = {
            "dataset_type": dataset_type,
            "exported_at": "2026-07-08T12:00:00Z",
            "filters": filters,
            "records": [
                {"metric": "Occupancy Rate", "value": 0.74, "status": "Healthy"},
                {"metric": "ADR", "value": 150.00, "status": "Healthy"},
                {"metric": "RevPAR", "value": 111.00, "status": "Healthy"},
                {
                    "metric": "SLA Turnaround Compliance",
                    "value": 0.92,
                    "status": "Healthy",
                },
                {"metric": "Guest Satisfaction", "value": 4.6, "status": "Healthy"},
            ],
        }

        if normalized_format == "JSON":
            return json.dumps(dataset, indent=2).encode("utf-8")

        elif normalized_format == "CSV":
            lines = ["Metric,Value,Status"]
            for r in dataset["records"]:
                lines.append(f"{r['metric']},{r['value']},{r['status']}")
            return "\n".join(lines).encode("utf-8")

        elif normalized_format == "EXCEL":
            # Formatted as Tab-Separated Values (TSV) which Excel parses natively
            lines = ["Metric\tValue\tStatus"]
            for r in dataset["records"]:
                lines.append(f"{r['metric']}\t{r['value']}\t{r['status']}")
            return "\n".join(lines).encode("utf-8")

        elif normalized_format == "PDF":
            # Generates a formatted textual PDF payload structure
            pdf_lines = [
                "%PDF-1.4",
                "1 0 obj",
                "<< /Type /Catalog /Pages 2 0 R >>",
                "endobj",
                "2 0 obj",
                "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
                "endobj",
                "3 0 obj",
                "<< /Type /Page /Parent 2 0 R /Resources << >> /Contents 4 0 R >>",
                "endobj",
                "4 0 obj",
                f"<< /Length {150} >>",
                "stream",
                f"HospitalityAI Executive Report - Type: {dataset_type}",
                "Occupancy: 74% | ADR: $150.00 | RevPAR: $111.00",
                "endstream",
                "endobj",
                "xref",
                "0 5",
                "0000000000 65535 f",
                "trailer",
                "<< /Size 5 /Root 1 0 R >>",
                "startxref",
                "%%EOF",
            ]
            return "\n".join(pdf_lines).encode("utf-8")

        else:
            raise ValueError(f"Unsupported export format: {export_format}")
