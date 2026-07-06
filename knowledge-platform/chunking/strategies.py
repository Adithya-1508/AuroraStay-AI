from typing import Any
from uuid import uuid4


class Chunk:
    """Represents a text chunk with metadata."""

    def __init__(
        self, chunk_id: str, document_id: str, content: str, metadata: dict[str, Any]
    ) -> None:
        self.chunk_id = chunk_id
        self.document_id = document_id
        self.content = content
        self.metadata = metadata


class ChunkingEngine:
    """Engine splitting text using recursive, fixed-size, or section strategies."""

    def fixed_size_split(
        self, text: str, chunk_size: int = 500, overlap: int = 50
    ) -> list[str]:
        """Splits text into fixed-size boundaries with overlap."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def recursive_split(
        self, text: str, chunk_size: int = 500, overlap: int = 50
    ) -> list[str]:
        """Recursively splits text to fit target token/character size."""
        paragraphs = text.split("\n\n")
        chunks = []
        current = ""
        for p in paragraphs:
            if len(current) + len(p) <= chunk_size:
                current += "\n\n" + p if current else p
            else:
                if current:
                    chunks.append(current)
                if len(p) > chunk_size:
                    sentences = p.split(". ")
                    for s in sentences:
                        if len(current) + len(s) <= chunk_size:
                            current += ". " + s if current else s
                        else:
                            if current:
                                chunks.append(current)
                            current = s
                else:
                    current = p
        if current:
            chunks.append(current)
        return chunks

    def section_split(self, text: str) -> list[dict[str, Any]]:
        """Splits text by Markdown headers into section blocks."""
        sections = []
        lines = text.splitlines()
        current_header = "Intro"
        current_lines: list[str] = []

        for line in lines:
            if line.startswith("#"):
                if current_lines:
                    sections.append(
                        {
                            "header": current_header,
                            "text": "\n".join(current_lines).strip(),
                        }
                    )
                    current_lines = []
                current_header = line.strip("# ").strip()
            else:
                current_lines.append(line)

        if current_lines or current_header:
            sections.append(
                {
                    "header": current_header,
                    "text": "\n".join(current_lines).strip(),
                }
            )

        return sections

    def chunk_document(
        self,
        text: str,
        document_id: str,
        source: str,
        version: str,
        strategy: str = "recursive",
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> list[Chunk]:
        """Decomposes text into a list of Chunk objects decorated with metadata."""
        chunks = []

        if strategy == "section":
            sections = self.section_split(text)
            for sec in sections:
                chunk_id = str(uuid4())
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        document_id=document_id,
                        content=sec["text"],
                        metadata={
                            "document_id": document_id,
                            "chunk_id": chunk_id,
                            "section": sec["header"],
                            "page": 1,
                            "heading": sec["header"],
                            "source": source,
                            "version": version,
                        },
                    )
                )
        else:
            if strategy == "fixed":
                split_texts = self.fixed_size_split(text, chunk_size, overlap)
            else:
                split_texts = self.recursive_split(text, chunk_size, overlap)

            for idx, block in enumerate(split_texts):
                chunk_id = str(uuid4())
                chunks.append(
                    Chunk(
                        chunk_id=chunk_id,
                        document_id=document_id,
                        content=block,
                        metadata={
                            "document_id": document_id,
                            "chunk_id": chunk_id,
                            "section": "General",
                            "page": 1,
                            "heading": f"Part {idx + 1}",
                            "source": source,
                            "version": version,
                        },
                    )
                )

        return chunks


__all__ = ["Chunk", "ChunkingEngine"]
