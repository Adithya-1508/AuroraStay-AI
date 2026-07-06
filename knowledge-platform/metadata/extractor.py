import re
from typing import Any


class MetadataExtractor:
    """Extractor pulling metadata parameters from raw document payloads."""

    def extract_metadata(self, text: str, source_path: str) -> dict[str, Any]:
        """Analyzes text properties to compile a metadata dictionary."""
        heading = "General"
        match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        if match:
            heading = match.group(1).strip()

        version = "1.0.0"
        ver_match = re.search(
            r"(?:version|v)\s*[:=]?\s*(\d+\.\d+\.\d+)", text, re.IGNORECASE
        )
        if ver_match:
            version = ver_match.group(1).strip()

        return {
            "source": source_path,
            "heading": heading,
            "version": version,
            "estimated_token_count": len(text) // 4,
            "char_length": len(text),
        }


__all__ = ["MetadataExtractor"]
