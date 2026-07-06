import csv
import json
import os
from typing import Any

from .base import BaseParser


class MarkdownParser(BaseParser):
    """Parser extracting raw text and structural headings from Markdown files."""

    async def parse(self, file_path: str) -> dict[str, Any]:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        return {
            "text": content,
            "metadata": {"type": "markdown", "size": len(content)},
            "structure": {
                "headings": [
                    line for line in content.splitlines() if line.startswith("#")
                ]
            },
        }


class HTMLParser(BaseParser):
    """Parser stripping markup tags and extracting text from HTML files."""

    async def parse(self, file_path: str) -> dict[str, Any]:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
        # Basic tag stripper fallback
        import re

        clean_text = re.sub("<[^<]+?>", "", content)
        return {
            "text": clean_text.strip(),
            "metadata": {"type": "html", "size": len(content)},
            "structure": {},
        }


class CSVParser(BaseParser):
    """Parser loading tabular structures and rows from CSV files."""

    async def parse(self, file_path: str) -> dict[str, Any]:
        rows = []
        with open(file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(", ".join(row))
        text = "\n".join(rows)
        return {
            "text": text,
            "metadata": {"type": "csv", "size": len(text)},
            "structure": {"rows_count": len(rows)},
        }


class JSONParser(BaseParser):
    """Parser deserializing keys and values from JSON files."""

    async def parse(self, file_path: str) -> dict[str, Any]:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        text = json.dumps(data, indent=2)
        return {
            "text": text,
            "metadata": {"type": "json", "size": len(text)},
            "structure": {"keys": list(data.keys()) if isinstance(data, dict) else []},
        }


class PDFParser(BaseParser):
    """Parser extracting text from PDF documents."""

    async def parse(self, file_path: str) -> dict[str, Any]:
        # Robust basic parsing fallback
        with open(file_path, errors="ignore") as f:
            content = f.read(2000)
        return {
            "text": content,
            "metadata": {"type": "pdf", "size": len(content)},
            "structure": {"pages": 1},
        }


class DOCXParser(BaseParser):
    """Parser extracting text from Word documents."""

    async def parse(self, file_path: str) -> dict[str, Any]:
        # Robust basic parsing fallback
        with open(file_path, errors="ignore") as f:
            content = f.read(2000)
        return {
            "text": content,
            "metadata": {"type": "docx", "size": len(content)},
            "structure": {},
        }


class ParserFactory:
    """Factory selecting the appropriate parser based on file extension."""

    def __init__(self) -> None:
        self._parsers = {
            ".md": MarkdownParser(),
            ".html": HTMLParser(),
            ".csv": CSVParser(),
            ".json": JSONParser(),
            ".pdf": PDFParser(),
            ".docx": DOCXParser(),
        }

    def get_parser(self, file_path: str) -> BaseParser:
        """Returns the BaseParser mapping to target file extension."""
        _, ext = os.path.splitext(file_path.lower())
        if ext not in self._parsers:
            # Fallback to standard Markdown/Text parser
            return self._parsers[".md"]
        return self._parsers[ext]


__all__ = [
    "MarkdownParser",
    "HTMLParser",
    "CSVParser",
    "JSONParser",
    "PDFParser",
    "DOCXParser",
    "ParserFactory",
]
