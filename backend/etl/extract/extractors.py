import csv
import json
from typing import Any


class CSVExtractor:
    """Extractor for flat CSV datasets."""

    def extract(self, file_path: str) -> list[dict[str, Any]]:
        """Parses CSV dataset rows into list of key/value maps."""
        records = []
        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
        return records


class JSONExtractor:
    """Extractor for structured JSON data dumps."""

    def extract(self, file_path: str) -> Any:
        """Loads and parses JSON files content."""
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)


class APIExtractor:
    """Mock extractor simulating REST API payload retrievals."""

    async def extract(self, url: str) -> Any:
        """Retrieves and parses API payloads."""
        # Simulated endpoint return payload for testing
        return {
            "success": True,
            "data": [
                {
                    "email": "sarah.jennings@example.com",
                    "first_name": "Sarah",
                    "last_name": "Jennings",
                    "phone": "555-0143",
                    "loyalty_tier": "Gold",
                }
            ],
        }


class PMSMockExtractor:
    """Mock Property Management System extractor yielding daily dumps."""

    def extract(self) -> list[dict[str, Any]]:
        """Yields raw guest and booking records dumps."""
        return [
            {
                "guest_email": "john.watson@example.com",
                "first_name": "John",
                "last_name": "Watson",
                "phone": "+1-555-0101",
                "room_number": "101",
                "room_category": "Standard",
                "check_in": "2026-07-10",
                "check_out": "2026-07-15",
                "total_cost": "750.00",
                "status": "Confirmed",
            },
            {
                "guest_email": "sherlock.holmes@example.com",
                "first_name": "Sherlock",
                "last_name": "Holmes",
                "phone": "+1-555-0221",
                "room_number": "221",
                "room_category": "Suite",
                "check_in": "2026-07-12",
                "check_out": "2026-07-20",
                "total_cost": "2400.00",
                "status": "Confirmed",
            },
        ]


__all__ = ["CSVExtractor", "JSONExtractor", "APIExtractor", "PMSMockExtractor"]
