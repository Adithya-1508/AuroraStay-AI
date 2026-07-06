# RAG Specification: Citation Engine

This document details citation formats and provenance rules.

## Citation Schema

Every retrieved chunk includes traceable provenance:
- `source_document`: File name or URL.
- `version`: Version string of the document.
- `page`: Page index (if available).
- `section`: Heading or paragraph details.

## Citation Tag Format

When formatting answers, the citation tag matches the structure:
`[DocName_v1_p2]` or `[DocName_v1_SecHeader]`

Answers must not be generated without corresponding source tags, ensuring verification checks can link text to its exact origin.
