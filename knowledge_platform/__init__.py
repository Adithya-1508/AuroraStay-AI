# ruff: noqa: E402
import os

# Redirect this package path to the hyphenated knowledge-platform folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
kp_path = os.path.join(parent_dir, "knowledge-platform")

__path__ = [kp_path]

# Export from redirected submodules
from knowledge_platform.chunking.strategies import Chunk, ChunkingEngine
from knowledge_platform.citations.generator import CitationGenerator
from knowledge_platform.embeddings.client import EmbeddingPipeline
from knowledge_platform.evaluation.metrics import RetrievalEvaluator
from knowledge_platform.indexing.qdrant import QdrantIndexer
from knowledge_platform.ingestion.service import KnowledgeIngestionService
from knowledge_platform.metadata.extractor import MetadataExtractor
from knowledge_platform.parsers.factory import ParserFactory
from knowledge_platform.reranking.service import BaseReranker, NvidiaReranker
from knowledge_platform.retrieval.engine import Retriever
from knowledge_platform.versioning.manager import KnowledgeVersioningManager

__all__ = [
    "ParserFactory",
    "ChunkingEngine",
    "MetadataExtractor",
    "EmbeddingPipeline",
    "QdrantIndexer",
    "Retriever",
    "BaseReranker",
    "NvidiaReranker",
    "CitationGenerator",
    "KnowledgeIngestionService",
    "KnowledgeVersioningManager",
    "RetrievalEvaluator",
    "Chunk",
]
