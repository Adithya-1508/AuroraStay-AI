import math
import os
from abc import ABC, abstractmethod
from typing import Any

import httpx
import structlog

logger = structlog.get_logger()


class BaseReranker(ABC):
    """Abstract base class standardizing reranking of retrieved documents."""

    @abstractmethod
    async def rerank(
        self, query: str, chunks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Reranks retrieved chunk list returning them sorted descending."""
        pass


class NvidiaReranker(BaseReranker):
    """Reranker implementing NVIDIA NIM rerank-qa-mistral-4b API calls."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://ai.api.nvidia.com/v1/retrieval/nvidia/reranking",
    ) -> None:
        self.api_key = api_key or os.environ.get("NVIDIA_API_KEY")
        self.base_url = base_url
        self.model = "nvidia/rerank-qa-mistral-4b"

    async def _fallback_rerank(
        self, query: str, chunks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Fallback local scoring based on term overlaps and normalized scores."""
        logger.info("Using local fallback scoring for reranker.")
        scored_chunks = []
        for c in chunks:
            content = c.get("content", "").lower()
            query_words = set(query.lower().split())
            content_words = set(content.split())
            overlap = len(query_words.intersection(content_words))
            boost = overlap * 0.1
            new_score = min(1.0, c.get("score", 0.5) + boost)
            scored_chunks.append({**c, "score": new_score})
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks

    async def rerank(
        self, query: str, chunks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Reranks retrieved context records using NVIDIA NIM or fallback logic."""
        if not chunks:
            return []

        if not self.api_key:
            return await self._fallback_rerank(query, chunks)

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "query": {"text": query},
                "passages": [{"text": c.get("content", "")} for c in chunks],
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(self.base_url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    rankings = data.get("rankings", [])
                    scored_chunks = []
                    for rank in rankings:
                        idx = rank["index"]
                        logit = rank.get("logit", 0.0)
                        norm_score = (
                            1.0 / (1.0 + math.exp(-logit))
                            if "logit" in rank
                            else rank.get("score", 0.5)
                        )

                        original_chunk = chunks[idx]
                        scored_chunks.append({**original_chunk, "score": norm_score})
                    return scored_chunks
                else:
                    logger.warn(
                        "NVIDIA NIM API failed. Using fallback reranking.",
                        status_code=res.status_code,
                    )
                    return await self._fallback_rerank(query, chunks)
        except Exception as e:
            logger.error("NVIDIA Reranker exception. Falling back.", error=str(e))
            return await self._fallback_rerank(query, chunks)


__all__ = ["BaseReranker", "NvidiaReranker"]
