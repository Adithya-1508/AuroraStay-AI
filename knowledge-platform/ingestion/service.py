import os
from uuid import uuid4

import structlog

from ..chunking.strategies import ChunkingEngine
from ..embeddings.client import EmbeddingPipeline
from ..indexing.qdrant import QdrantIndexer
from ..metadata.extractor import MetadataExtractor
from ..parsers.factory import ParserFactory
from ..versioning.manager import KnowledgeVersioningManager

logger = structlog.get_logger()


class KnowledgeIngestionService:
    """Service orchestrating ingestion parsing, chunking, and database indexing."""

    def __init__(
        self,
        indexer: QdrantIndexer,
        embedding_pipeline: EmbeddingPipeline,
        version_manager: KnowledgeVersioningManager,
    ) -> None:
        self.indexer = indexer
        self.embedding_pipeline = embedding_pipeline
        self.version_manager = version_manager

        self.parser_factory = ParserFactory()
        self.chunking_engine = ChunkingEngine()
        self.metadata_extractor = MetadataExtractor()

    async def ingest(
        self,
        file_path: str,
        collection_name: str = "hotel-knowledge",
        strategy: str = "recursive",
        chunk_size: int = 500,
        overlap: int = 50,
    ) -> str:
        """Processes document and indexes chunks into database namespace."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Target file not found: {file_path}")

        logger.info("Beginning document ingestion pipeline", file=file_path)

        parser = self.parser_factory.get_parser(file_path)
        parsed_doc = await parser.parse(file_path)
        text = parsed_doc["text"]

        meta = self.metadata_extractor.extract_metadata(text, file_path)
        doc_version = meta["version"]

        document_id = str(uuid4())
        chunks = self.chunking_engine.chunk_document(
            text=text,
            document_id=document_id,
            source=file_path,
            version=doc_version,
            strategy=strategy,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        chunk_texts = [c.content for c in chunks]
        embeddings = await self.embedding_pipeline.get_embeddings_batch(chunk_texts)

        await self.indexer.create_collection(collection_name)
        await self.indexer.upsert_chunks(collection_name, chunks, embeddings)

        chunk_version_sig = f"{strategy}_{chunk_size}_{overlap}"
        self.version_manager.register_version(
            document_id=document_id,
            doc_version=doc_version,
            embedding_version=self.embedding_pipeline.model_version,
            chunk_version=chunk_version_sig,
            index_version=collection_name,
        )

        logger.info(
            "Document ingestion completed successfully",
            document_id=document_id,
            chunks_count=len(chunks),
            version=doc_version,
        )

        return document_id


__all__ = ["KnowledgeIngestionService"]
