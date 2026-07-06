from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class GuestBaseEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1


class GuestProfileUpdated(GuestBaseEvent):
    guest_id: UUID
    updated_fields: list[str]


class PreferenceChanged(GuestBaseEvent):
    guest_id: UUID
    changed_preferences: dict[str, str]


class ConversationStarted(GuestBaseEvent):
    conversation_id: UUID
    guest_id: UUID | None


class ConversationEnded(GuestBaseEvent):
    conversation_id: UUID
    guest_id: UUID | None
    duration_seconds: int


class RecommendationGenerated(GuestBaseEvent):
    recommendation_id: UUID
    guest_id: UUID
    item_type: str
    score: float


class IssueReported(GuestBaseEvent):
    guest_id: UUID
    issue_type: str
    description: str


class ServiceRequested(GuestBaseEvent):
    guest_id: UUID
    service_type: str
    details: dict[str, str]


class EscalationRequested(GuestBaseEvent):
    guest_id: UUID
    conversation_id: UUID
    reason: str
