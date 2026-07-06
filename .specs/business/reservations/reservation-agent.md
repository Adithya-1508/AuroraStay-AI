# Spec: Reservation Assistant Agent

- **Status**: Draft
- **Owner**: Agent Engineering Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-06

## 1. Purpose
Define the business agent that acts as a Reservation Assistant to help guests book, modify, or cancel rooms, suggest upgrades, and answer reservation questions.

## 2. Responsibilities
- Understand natural language queries related to reservations.
- Delegate actions to registered tools using LangGraph routing.
- Never call LLM models directly—route all prompts and calls through the `AIService`.
- Enforce business rules and permissions before invoking operations.

## 3. Dependencies
- **AI Platform**: For text generation and tool routingAdapter.
- **Knowledge Platform**: For RAG search on reservation policies (e.g. cancellation policy FAQ).
- **Reservation Services**: Under the business core layer.

## 4. Interfaces
```python
class ReservationAssistantAgent(BaseAgent):
    name = "ReservationAssistant"
    version = "1.0.0"
    description = "AI Agent assisting with hotel room reservations, availability, pricing, upgrades, and cancellations."
    
    # Declarations of tools
    required_tools = [
        "SearchAvailabilityTool",
        "CalculatePriceTool",
        "ReserveRoomTool",
        "ModifyReservationTool",
        "CancelReservationTool",
        "RecommendUpgradeTool"
    ]
    
    async def chat(self, session_id: str, message: str) -> AgentResponse:
        """Processes conversational input through the LangGraph engine."""
        pass
```

### System Prompt Version
`reservation_assistant_v1.0`:
> You are the HospitalityAI Reservation Assistant. Your role is to assist guests with bookings, modifications, cancellations, pricing estimates, and room upgrades. You must always use tools to execute actions or retrieve availability. Never guess or fabricate availability. When answering questions about policies (e.g., cancellation policy), retrieve answers from the Knowledge Platform.

## 5. Configuration
- `LLM_MODEL`: Map to `meta/llama3-70b-instruct` or fallback.
- `RECURSION_LIMIT`: LangGraph recursion check limit, default 25.

## 6. Error Handling
- Return clear, helpful guidance when tool calls fail.
- Gracefully handle unauthorized actions by requesting user details or staff support.

## 7. Security
- Enforce JWT authentication checking when a guest attempts to view or modify an active reservation.

## 8. Testing
- **Agent Simulation Tests**:
  - Test routing decisions (e.g., user says "I want to cancel" -> routes to `CancelReservationTool` or policy retrieve).
  - Test retrieval fallback when knowledge matches are below threshold.

## 9. Acceptance Criteria
- [ ] Uses LangGraph to orchestrate goals.
- [ ] Executes operations purely through tools.
- [ ] Resolves policy questions using the Knowledge Platform.
