# Domain Glossary (Ubiquitous Language)

This glossary defines the canonical business terms used throughout HospitalityAI's codebase, specifications, user interfaces, and LLM prompts.

---

## 1. Guest
- **Definition**: An individual who registers, books, or occupies a room or utilizes hotel services.
- **Business Meaning**: The primary customer. Their satisfaction governs service flows and VIP recommendation triggers.
- **Context**: Guest Management / CRM.
- **Synonyms**: Patron, Client, Visitor.
- **Forbidden Terminology**: "User" (except in technical authentication context), "Tenant" (causes confusion with multi-property systems).
- **Related Concepts**: [Reservation](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/aggregates.md#reservation), [LoyaltyTier](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/value-objects.md#loyaltytier).

---

## 2. Reservation
- **Definition**: A secured contract guaranteeing a room allocation for a specified date range and price.
- **Business Meaning**: The core transactional record tracking inventory commitment and expected revenue.
- **Context**: Reservation Management.
- **Synonyms**: Room Booking.
- **Forbidden Terminology**: "Registration" (which refers specifically to physical arrival/check-in).
- **Related Concepts**: [Stay](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#stay), [Room](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#room).

---

## 3. Booking
- **Definition**: Synonym for [Reservation](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#reservation).
- **Business Meaning**: Used in customer-facing flows (e.g. "Create Booking").
- **Context**: Front-end Chat/Web interfaces.
- **Synonyms**: Reservation.
- **Forbidden Terminology**: None.
- **Related Concepts**: [Reservation](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#reservation).

---

## 4. Stay
- **Definition**: The active state of a reservation when the guest is physically registered and occupying the room.
- **Business Meaning**: The period of physical hospitality, during which housekeeping and concierge services are utilized.
- **Context**: Front Desk Operations.
- **Synonyms**: Active Booking, Occupancy period.
- **Forbidden Terminology**: "Visit" (too ambiguous, could refer to a spa visit).
- **Related Concepts**: [CheckIn](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-events.md#guestcheckedin), [CheckOut](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-events.md#guestcheckedout).

---

## 5. Room
- **Definition**: An individual physical space within the hotel inventory.
- **Business Meaning**: The inventory asset that generates revenue.
- **Context**: Inventory / Housekeeping.
- **Synonyms**: Rental unit.
- **Forbidden Terminology**: "Suite" (when referring to generic rooms; Suite is a specific Room Category).
- **Related Concepts**: [Room Category](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#room-category), [Housekeeping](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#housekeeping).

---

## 6. Room Category
- **Definition**: A grouping of rooms sharing identical configurations, capacities, and pricing brackets (e.g., Single, Deluxe, Suite).
- **Business Meaning**: The unit of product selection for guest reservations.
- **Context**: Product Catalog.
- **Synonyms**: Room Type.
- **Forbidden Terminology**: "Room Class", "Tier".
- **Related Concepts**: [Room](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#room).

---

## 7. Availability
- **Definition**: The count of vacant, clean, and unbooked rooms in a Room Category for a specific DateRange.
- **Business Meaning**: The pool of sellable inventory.
- **Context**: Reservation Search.
- **Synonyms**: Vacancy.
- **Forbidden Terminology**: "Empty rooms" (empty dirty rooms are not available for booking).
- **Related Concepts**: [DateRange](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/value-objects.md#daterange).

---

## 8. Rate Plan
- **Definition**: A set of rules linking a Room Category stay to nightly prices, policies, and inclusions (e.g., "Bed & Breakfast", "Non-Refundable").
- **Business Meaning**: The product pricing model.
- **Context**: Revenue Management.
- **Synonyms**: Pricing Scheme.
- **Forbidden Terminology**: "Discount code".
- **Related Concepts**: [Pricing](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#pricing).

---

## 9. Pricing
- **Definition**: The nightly monetary cost calculated for a reservation.
- **Business Meaning**: The revenue yield value of room nights.
- **Context**: Billing / Revenue.
- **Synonyms**: Rate, Cost.
- **Forbidden Terminology**: "Charge" (which includes taxes and spa incidents).
- **Related Concepts**: [Money](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/value-objects.md#money).

---

## 10. Occupancy
- **Definition**: The ratio of occupied rooms to total available physical rooms, expressed as a percentage.
- **Business Meaning**: The primary utilization metric for measuring hotel demand.
- **Context**: Analytics / Revenue.
- **Synonyms**: Occupancy Rate.
- **Forbidden Terminology**: "Fill level".
- **Related Concepts**: [Forecast](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#forecast).

---

## 11. Revenue
- **Definition**: Cumulative room rates and incidental service earnings during a calendar interval.
- **Business Meaning**: The core financial metric (ADR, RevPAR).
- **Context**: Analytics / Executive Dashboard.
- **Synonyms**: Yield, Turnover, Earnings.
- **Forbidden Terminology**: "Profit" (which deducts operating costs).
- **Related Concepts**: [RevPAR](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/bounded-contexts.md#revenue-context).

---

## 12. Forecast
- **Definition**: An ML prediction model output outlining expected future occupancy and cancellations for the next 30 days.
- **Business Meaning**: Enables revenue managers to adjust rate plans dynamically.
- **Context**: Analytics / ML.
- **Synonyms**: Demand Prediction.
- **Forbidden Terminology**: "Guess", "Speculation".
- **Related Concepts**: [Occupancy](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#occupancy).

---

## 13. Recommendation
- **Definition**: An AI/ML-generated proposal (e.g., room upgrade or rate plan adjustment).
- **Business Meaning**: Assists staff or guests in optimizing decisions.
- **Context**: Decision Intelligence / AI Concierge.
- **Synonyms**: System Suggestion.
- **Forbidden Terminology**: "Action" (a recommendation is non-binding until accepted).
- **Related Concepts**: [Decision](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#decision).

---

## 14. Decision
- **Definition**: An explicit staff action accepting or rejecting a system recommendation.
- **Business Meaning**: Creates audit logs and triggers system overrides (e.g., changing room prices).
- **Context**: Decision Intelligence.
- **Synonyms**: Approval / Rejection.
- **Forbidden Terminology**: None.
- **Related Concepts**: [Recommendation](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#recommendation).

---

## 15. Task
- **Definition**: An operational unit of work assigned to a staff member (e.g., clean room 302).
- **Business Meaning**: Tracks operational efficiency and completion status.
- **Context**: Operations / Housekeeping.
- **Synonyms**: Work Item.
- **Forbidden Terminology**: "Job" (too broad, refers to employment).
- **Related Concepts**: [Work Order](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#work-order).

---

## 16. Work Order
- **Definition**: Synonym for [Task](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#task) inside Maintenance and Housekeeping queues.
- **Business Meaning**: Represents a formal request for service.
- **Context**: Facilities / Operations.
- **Synonyms**: Maintenance Request.
- **Forbidden Terminology**: None.
- **Related Concepts**: [Maintenance](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#maintenance).

---

## 17. Conversation
- **Definition**: A sequence of natural language messages exchanged between a guest and the AI Concierge.
- **Business Meaning**: The interface for guest self-service.
- **Context**: AI Concierge / Chat.
- **Synonyms**: Chat Session, Session.
- **Forbidden Terminology**: "Thread".
- **Related Concepts**: [AI Concierge](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#ai-concierge).

---

## 18. Knowledge Base
- **Definition**: A repository of hotel FAQ text files, policy documents, and amenity listings.
- **Business Meaning**: The verified data source used for RAG generation.
- **Context**: Knowledge Platform / RAG.
- **Synonyms**: Reference Docs.
- **Forbidden Terminology**: "Training Set" (knowledge base is retrieved dynamically, not used to train the base LLM).
- **Related Concepts**: [AI Concierge](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#ai-concierge).

---

## 19. Housekeeping
- **Definition**: The business department responsible for cleaning, sanitizing, and preparing rooms.
- **Business Meaning**: Direct impact on room availability pace.
- **Context**: Operations.
- **Synonyms**: Cleaning Service.
- **Forbidden Terminology**: None.
- **Related Concepts**: [Room](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#room).

---

## 20. Maintenance
- **Definition**: The business department responsible for building repairs and room equipment servicing.
- **Business Meaning**: Resolves physical issues that put rooms Out of Order.
- **Context**: Operations.
- **Synonyms**: Facilities Repair.
- **Forbidden Terminology**: None.
- **Related Concepts**: [Work Order](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#work-order).

---

## 21. Restaurant
- **Definition**: The hotel's dining facilities.
- **Business Meaning**: An incidental revenue stream.
- **Context**: Operations.
- **Synonyms**: Dining.
- **Forbidden Terminology**: None.
- **Related Concepts**: [Spa](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#spa).

---

## 22. Spa
- **Definition**: The hotel's wellness and spa treatment facility.
- **Business Meaning**: An incidental revenue stream.
- **Context**: Operations.
- **Synonyms**: Wellness Center.
- **Forbidden Terminology**: None.
- **Related Concepts**: [Restaurant](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#restaurant).

---

## 23. AI Concierge
- **Definition**: The conversational agent assisting guests with FAQs and booking services.
- **Business Meaning**: The automated customer service channel.
- **Context**: AI Platform.
- **Synonyms**: Virtual Assistant, Chatbot.
- **Forbidden Terminology**: "Robot".
- **Related Concepts**: [Conversation](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#conversation).

---

## 24. Executive Dashboard
- **Definition**: The analytics visualization screen exposing aggregated operational and revenue statistics.
- **Business Meaning**: Provides business intelligence for management decision-making.
- **Context**: Analytics / Executive Intelligence.
- **Synonyms**: Management Portal.
- **Forbidden Terminology**: "Console".
- **Related Concepts**: [Revenue](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#revenue).

---

## 25. Alert
- **Definition**: A system-generated warning indicating an exception condition (e.g. negative sentiment, high cancellation rates, delayed task).
- **Business Meaning**: Flags items requiring human staff attention.
- **Context**: Observability / Decision Intelligence.
- **Synonyms**: Notification, Warning.
- **Forbidden Terminology**: "Alarm".
- **Related Concepts**: [Decision](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/domain-glossary.md#decision).
