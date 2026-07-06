from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, BaseEntity


class KnowledgeDocument(Base, BaseEntity):
    """KnowledgeDocument table mapping database representation."""

    __tablename__ = "knowledge_documents"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)


__all__ = ["KnowledgeDocument"]
