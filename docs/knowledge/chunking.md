# Text Chunking Manual

The `ChunkingEngine` segments text documents into granular content blocks formatted with complete metadata.

## Strategies

- **Fixed-Size splitting**: Segments by character count thresholds with overlaps.
- **Recursive character splitting**: Splits recursively on structural boundaries (paragraphs, sentences).
- **Section splitting**: Creates chunks divided by Markdown header blocks.
