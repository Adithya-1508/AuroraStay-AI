from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    """Abstract base class representing a document parser."""

    @abstractmethod
    async def parse(self, file_path: str) -> dict[str, Any]:
        """Parses the target file, returning extracted text, metadata, and structure."""
        pass


__all__ = ["BaseParser"]
