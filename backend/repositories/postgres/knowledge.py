from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.knowledge_document import KnowledgeDocument
from backend.repositories.knowledge import AbstractKnowledgeRepository
from backend.repositories.postgres.base import PostgresRepository


class KnowledgeRepository(
    PostgresRepository[KnowledgeDocument], AbstractKnowledgeRepository
):
    """Postgres concrete repository managing KnowledgeDocument records persistence."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, KnowledgeDocument)

    async def get_by_category(self, category: str) -> Sequence[KnowledgeDocument]:
        """Retrieves all active knowledge documents under a specific category."""
        stmt = select(KnowledgeDocument).filter_by(category=category, is_deleted=False)
        result = await self.session.execute(stmt)
        return result.scalars().all()


__all__ = ["KnowledgeRepository"]
