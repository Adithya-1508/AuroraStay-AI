# Spec: AI Concierge & Chat Workflows

- **Status**: Ready
- **Owner**: RAG & AI Platform Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the business policies and flow controls governing conversational FAQ retrieval, RAG boundaries, and staff-escalation procedures.

## 2. Responsibilities
- Parse conversational natural language inputs from guests.
- Coordinate with the Knowledge Platform to fetch relevant context blocks.
- Block hallucinations by forcing the LLM to answer *only* using retrieved data.
- Detect handoff intents (explicit request for human help, angry sentiment, or system-unsupported tasks like payments).
- Transition session state to physical front desk queues upon handoff detection.

## 3. Dependencies
- **Knowledge Platform**: For document chunk retrieval.
- **AI Platform**: For LLM invocations and token tracking.
- **Observability**: For tracing query-context-response flows.

## 4. Interfaces
```python
# Conceptual interfaces for AI Concierge Service

class AIConciergeService:
    async def chat_response(
        self, session_id: str, guest_id: str, message: str
    ) -> ChatResponseSchema:
        """Processes message, retrieves FAQ context, generates LLM response, and checks handoff triggers."""
        pass

    async def escalate_to_staff(
        self, session_id: str, reason: str
    ) -> HandoffRecordSchema:
        """Updates chat session state to 'Staff-Controlled' and creates alert in front desk dashboard."""
        pass
```

## 5. Configuration
- `RAG_SIMILARITY_THRESHOLD`: Floating-point cut-off score (e.g. 0.75) for accepting Vector DB search results.
- `MAX_CHAT_HISTORY_WINDOW`: Number of previous messages passed to the LLM for conversation context.
- `HANDOFF_KEYWORDS`: Set of terms triggers (e.g. "manager", "complaint", "human").

## 6. Error Handling
- `RAGContextNotFoundError`: Raised when similarity searches return no results. Generates a polite fallback response offering staff handoff.
- `LLMTimeoutError`: Fallback to static text message apologizing for network delays.
- `ContentSafetyViolation`: Raised when guest input fails toxicity checks.

## 7. Security
- Restrict retrieval queries so that search scopes are restricted to general FAQs and the current guest's reservation data.
- Scrub sensitive details (credit cards, personal documents) from prompt histories.

## 8. Testing
- **AI Evaluation**:
  - Run regression evaluation test sets checking RAG answers against Ground Truth FAQs.
  - Verify that the agent rejects questions not present in the FAQ guidelines.
- **Staff Queue Tests**:
  - Verify that escalation queries immediately trigger dashboard alerts.

## 9. Acceptance Criteria
- [ ] Agent refrains from inventing answers when context is missing.
- [ ] Explicit human-receptionist request escalates within $\le 500\text{ ms}$.
- [ ] Chat window is locked for guest input when session changes to `Staff-Controlled` status.
