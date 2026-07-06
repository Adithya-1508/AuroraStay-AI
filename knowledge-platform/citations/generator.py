import os
from typing import Any


class CitationGenerator:
    """Citation engine standardizing provenance formatting tag templates."""

    def generate_tag(self, metadata: dict[str, Any]) -> str:
        """Compiles metadata parameters into standardized [DocName_v1_p2] trace tags."""
        source = metadata.get("source", "unknown")
        basename = os.path.basename(source)
        doc_name, _ = os.path.splitext(basename)

        doc_name = doc_name.replace(" ", "_")
        version = metadata.get("version", "v1.0.0").replace(".", "_")
        page = metadata.get("page")
        section = metadata.get("section", "General").replace(" ", "_")

        if page is not None and str(page).isdigit():
            return f"[{doc_name}_{version}_p{page}]"
        return f"[{doc_name}_{version}_{section}]"

    def format_citation(self, chunk: dict[str, Any]) -> dict[str, Any]:
        """Decorates retrieved context record with generated citation details."""
        metadata = chunk.get("metadata", {})
        tag = self.generate_tag(metadata)

        citation_details = {
            "source_document": os.path.basename(metadata.get("source", "unknown")),
            "version": metadata.get("version", "1.0.0"),
            "page": metadata.get("page"),
            "section": metadata.get("section", "General"),
            "confidence_score": chunk.get("score", 0.0),
            "citation_tag": tag,
        }

        return {**chunk, "citation": citation_details}


__all__ = ["CitationGenerator"]
