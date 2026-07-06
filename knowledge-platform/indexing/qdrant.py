import math
from typing import Any

import structlog

logger = structlog.get_logger()


class QdrantIndexer:
    """Vector database index manager with built-in cosine similarity fallback mocks."""

    def __init__(
        self, host: str = "localhost", port: int = 6333, use_mock: bool = True
    ) -> None:
        self.use_mock = use_mock
        # collection_name -> list of records
        self._mock_db: dict[str, list[dict[str, Any]]] = {}

        if not use_mock:
            try:
                from qdrant_client import QdrantClient

                self.client = QdrantClient(host=host, port=port)
            except Exception as e:
                logger.error(
                    "Failed to connect to Qdrant. Falling back to mock.",
                    error=str(e),
                )
                self.use_mock = True

    async def create_collection(
        self, collection_name: str, vector_size: int = 1536
    ) -> None:
        """Creates a collection partition schema if missing."""
        if self.use_mock:
            self._mock_db[collection_name] = []
            return

        from qdrant_client.models import Distance, VectorParams

        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
        except Exception as e:
            logger.debug("Collection creation bypassed", error=str(e))

    async def upsert_chunks(
        self, collection_name: str, chunks: list[Any], embeddings: list[list[float]]
    ) -> None:
        """Inserts or updates vector points and payloads in namespace."""
        if self.use_mock:
            if collection_name not in self._mock_db:
                self._mock_db[collection_name] = []
            for chunk, vector in zip(chunks, embeddings, strict=True):
                self._mock_db[collection_name].append(
                    {
                        "id": chunk.chunk_id,
                        "vector": vector,
                        "payload": {"content": chunk.content, **chunk.metadata},
                    }
                )
            return

        from qdrant_client.models import PointStruct

        points = []
        for chunk, vector in zip(chunks, embeddings, strict=True):
            points.append(
                PointStruct(
                    id=chunk.chunk_id,
                    vector=vector,
                    payload={"content": chunk.content, **chunk.metadata},
                )
            )
        self.client.upsert(collection_name=collection_name, points=points)

    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        filter_meta: dict[str, Any] | None = None,
        top_k: int = 3,
    ) -> list[dict[str, Any]]:
        """Queries Qdrant matching criteria filters."""
        if self.use_mock:
            if collection_name not in self._mock_db:
                return []

            results = []

            def cosine_similarity(v1: list[float], v2: list[float]) -> float:
                sum_xx, sum_yy, sum_xy = 0.0, 0.0, 0.0
                for x, y in zip(v1, v2, strict=True):
                    sum_xx += x * x
                    sum_yy += y * y
                    sum_xy += x * y
                if sum_xx == 0.0 or sum_yy == 0.0:
                    return 0.0
                return sum_xy / (math.sqrt(sum_xx) * math.sqrt(sum_yy))

            for item in self._mock_db[collection_name]:
                matched = True
                if filter_meta:
                    for k, v in filter_meta.items():
                        if item["payload"].get(k) != v:
                            matched = False
                            break
                if not matched:
                    continue

                score = cosine_similarity(query_vector, item["vector"])
                results.append(
                    {
                        "id": item["id"],
                        "score": score,
                        "payload": item["payload"],
                    }
                )

            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:top_k]

        from qdrant_client.models import FieldCondition, Filter, MatchValue

        qdrant_filter = None
        if filter_meta:
            conditions = [
                FieldCondition(key=k, match=MatchValue(value=v))
                for k, v in filter_meta.items()
            ]
            qdrant_filter = Filter(must=conditions)

        search_res = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=qdrant_filter,
            limit=top_k,
        )
        return [
            {"id": hit.id, "score": hit.score, "payload": hit.payload}
            for hit in search_res
        ]


__all__ = ["QdrantIndexer"]
