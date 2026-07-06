import uuid
from datetime import datetime
from typing import Any

import structlog
from knowledge_platform.retrieval.engine import Retriever
from sqlalchemy import select

from backend.models.conversation import Conversation
from backend.repositories.unit_of_work import AbstractUnitOfWork
from business.guest.events.publisher import domain_event_publisher
from business.guest.events.schemas import (
    ConversationStarted,
    EscalationRequested,
    IssueReported,
    ServiceRequested,
)
from business.guest.services.preferences import PreferenceLearningEngine

logger = structlog.get_logger()


class ConciergeService:
    """Concierge Service coordinating multi-turn chat, RAG, tool executions, and staff escalations."""

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        preference_engine: PreferenceLearningEngine,
        retriever: Retriever | None = None,
        reranker: Any = None,
    ) -> None:
        self.uow = uow
        self.preference_engine = preference_engine
        self.retriever = retriever
        self.reranker = reranker

    async def get_or_create_conversation(
        self, conversation_id: uuid.UUID, guest_id: uuid.UUID | None = None
    ) -> Conversation:
        """Retrieves an existing conversation session or initializes a new one."""
        async with self.uow:
            stmt = select(Conversation).filter_by(id=conversation_id)
            convs = await self.uow.session.execute(stmt)
            conv = convs.scalar_one_or_none()

            if not conv:
                conv = Conversation(
                    id=conversation_id,
                    guest_id=guest_id,
                    channel="WebChat",
                    messages={"messages": []},
                )
                self.uow.session.add(conv)
                await self.uow.commit()

                # Publish event
                await domain_event_publisher.publish(
                    ConversationStarted(
                        conversation_id=conversation_id,
                        guest_id=guest_id,
                    )
                )

            return conv

    async def chat(
        self, conversation_id: uuid.UUID, guest_id: uuid.UUID | None, text: str
    ) -> dict[str, Any]:
        """Processes user message, performs RAG retrieval, runs tool routes, and generates response."""
        # 1. Fetch or create conversation
        conv = await self.get_or_create_conversation(conversation_id, guest_id)

        # 2. Learn preferences dynamically from text (if guest exists)
        if guest_id:
            await self.preference_engine.learn_preferences_from_text(guest_id, text)

        # 3. Detect intent & formulate answer
        text_lower = text.lower()
        response_text = ""
        citations = []
        actions = []
        is_escalated = False

        # Node A: Handoff/Escalation
        if any(
            w in text_lower for w in ["escalate", "staff", "human", "help", "manager"]
        ):
            response_text = "I am escalating your request to a member of our hotel staff. They will contact you shortly."
            is_escalated = True
            actions.append("escalate_to_staff")
            if guest_id:
                await domain_event_publisher.publish(
                    EscalationRequested(
                        guest_id=guest_id,
                        conversation_id=conversation_id,
                        reason="Guest requested human assistance.",
                    )
                )

        # Node B: Check checkout policy / FAQs
        elif (
            "checkout" in text_lower
            or "check out" in text_lower
            or "check in" in text_lower
            or "check-in" in text_lower
            or "policy" in text_lower
            or "faq" in text_lower
        ):
            if self.retriever:
                try:
                    rag_results = await self.retriever.retrieve(text)
                    if rag_results:
                        response_text = rag_results[0]["content"]
                        citations.append(
                            f"{rag_results[0]['metadata'].get('document_name', 'FAQ')}_v1_p1"
                        )
                except Exception as e:
                    logger.warning(
                        "RAG retrieval failed, falling back to default.", error=str(e)
                    )

            if not response_text:
                # Local fallback
                response_text = "Standard check-in time is at 3:00 PM, and checkout time is at 11:00 AM."
                citations.append("FAQ_HotelPolicy_v1_p1")

        # Node C: Service booking (Room Service / Spa)
        elif any(w in text_lower for w in ["room service", "spa", "massage", "book"]):
            if "spa" in text_lower or "massage" in text_lower:
                response_text = "I would be happy to book a Spa Therapy session for you. I've logged this request."
                actions.append("book_spa")
                if guest_id:
                    await domain_event_publisher.publish(
                        ServiceRequested(
                            guest_id=guest_id,
                            service_type="Spa Booking",
                            details={"request": text},
                        )
                    )
            else:
                response_text = "I have submitted your room service request. It will be delivered to your room shortly."
                actions.append("room_service_request")
                if guest_id:
                    await domain_event_publisher.publish(
                        ServiceRequested(
                            guest_id=guest_id,
                            service_type="Room Service",
                            details={"request": text},
                        )
                    )

        # Node D: Issue reported
        elif any(
            w in text_lower for w in ["broken", "dirty", "leak", "fail", "complaint"]
        ):
            response_text = "I am so sorry to hear that. I have logged this issue and notified housekeeping immediately."
            actions.append("report_issue")
            if guest_id:
                await domain_event_publisher.publish(
                    IssueReported(
                        guest_id=guest_id,
                        issue_type="Maintenance/Housekeeping",
                        description=text,
                    )
                )

        # Node E: Standard friendly response
        else:
            response_text = "Hello! I am your AuroraStay Concierge. How can I assist you with your stay today?"

        # 4. Save message history
        history: list[dict[str, Any]] = []
        if isinstance(conv.messages, dict) and "messages" in conv.messages:
            history = list(conv.messages["messages"])
        history.append(
            {
                "sender": "guest",
                "text": text,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        history.append(
            {
                "sender": "assistant",
                "text": response_text,
                "timestamp": datetime.utcnow().isoformat(),
                "citations": citations,
                "actions": actions,
                "escalated": is_escalated,
            }
        )

        async with self.uow:
            # Re-fetch inside active transaction
            db_conv = await self.uow.session.get(Conversation, conversation_id)
            if db_conv:
                db_conv.messages = {"messages": history}
                await self.uow.commit()

        return {
            "reply": response_text,
            "citations": citations,
            "actions": actions,
            "escalated": is_escalated,
        }
