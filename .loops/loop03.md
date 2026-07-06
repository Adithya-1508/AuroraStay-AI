🚀 Loop 03 — Domain Modeling & Ubiquitous Language

Now we start the actual software design. This is one of the most important loops because everything else (database, APIs, agents, ML, UI) depends on getting the domain right.

The goal of Loop 03 is not to design tables or APIs. It is to define the business language and core business model.

Deliverables:

docs/domain/
├── README.md
├── ubiquitous-language.md
├── bounded-contexts.md
├── domain-model.md
├── business-rules.md
├── domain-events.md
├── aggregates.md
├── value-objects.md
├── entities.md
├── workflows.md
└── glossary.md

Antigravity should identify and model concepts such as:

Guest
Reservation
Room
RoomType
Booking
Stay
Payment (future placeholder)
Restaurant
RestaurantReservation
Spa
SpaAppointment
Employee
HousekeepingTask
MaintenanceTask
Review
Conversation
AIRequest
AIResponse
KnowledgeDocument
Embedding
Forecast
Recommendation
Notification

For each entity it must define:

Purpose
Responsibilities
Attributes
Relationships
Invariants (what must always be true)
Lifecycle
Ownership

It should also identify bounded contexts, for example:

Guest Management
Reservation Management
Hotel Operations
AI Platform
Knowledge Platform
Analytics & Forecasting

Each context should own its own business concepts and expose clear interfaces rather than sharing internal details.

The loop should produce domain workflows such as:

Guest booking a room
Guest asking the AI concierge a question
Housekeeping task creation after checkout
Revenue forecast generation
Knowledge document ingestion into the RAG pipeline

Domain model should automatically generate

.specs/database/

guest.md

reservation.md

room.md

review.md

conversation.md

Every entity gets its own specification.

Finally, this loop should establish the project's ubiquitous language: a glossary of canonical terms so that "Reservation", "Booking", "Stay", "Guest", and similar concepts always have one agreed meaning throughout the codebase, documentation, and AI prompts.

Exit criteria: by the end of Loop 03, there should be enough domain knowledge that Loop 04 can design the repository structure, database schema, and service interfaces without needing to redefine business concepts.