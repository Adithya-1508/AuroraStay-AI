# GEP Agent Workflows & Tools

The GEP utilizes a custom `GuestConciergeAgent` built on the LangGraph framework. It allows the model to act as a luxury concierge with a suite of specialized tools.

## Agent Architecture

* **Planner**: Decomposes natural language guest goals into dependency-aware execution steps.
* **Executor**: Runs tools concurrently to satisfy steps.
* **Workflow Engine**: Acompiled LangGraph state machine tracking agent progress.

## GEP Tools Directory

1. **SearchHotelKnowledgeTool**:
   Queries policy knowledge base / FAQs.
2. **FindRestaurantTool**:
   Queries menu, location, and hours of on-site/local restaurants.
3. **FindSpaServiceTool**:
   Retrieves available hotel spa services.
4. **RecommendFacilityTool**:
   Recommends hotel amenities tailored to guest profiles.
5. **ReservationLookupTool**:
   Checks active reservation dates and status.
6. **GuestPreferenceTool**:
   Explicitly registers pillow/room preference adjustments.
7. **EscalateToStaffTool**:
   Flags conversation for manual hotel staff review.
