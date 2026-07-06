LOOP 11 — Guest Experience Platform

Version: 1.0

Project: HospitalityAI

Status: Mandatory

Prerequisites

Loop 00 — Constitution
Loop 01 — Product Requirements
Loop 02 — Architecture
Loop 03 — Domain Modeling
Loop 04 — Repository Bootstrap
Loop 05 — Backend Core Platform
Loop 06 — Data Platform
Loop 07 — AI Platform
Loop 08 — Multi-Agent Platform
Loop 09 — Knowledge Platform
Loop 10 — Intelligent Reservation Platform
Purpose

Develop the Guest Experience Platform, the AI-powered interface between guests and the hotel.

This loop transforms HospitalityAI from an internal reservation system into a complete guest-facing intelligent platform.

Guests should be able to naturally communicate with HospitalityAI before, during, and after their stay.

Philosophy

HospitalityAI should behave like a luxury hotel concierge—not a chatbot.

The AI should understand guest context, personalize interactions, remember preferences, and coordinate with backend services while remaining transparent, reliable, and explainable.

Objectives

Build a complete Guest Experience Platform capable of:

Personalized AI conversations
Guest profile management
Preference learning
Recommendation generation
Hotel knowledge retrieval
Service discovery
Itinerary assistance
Conversation memory
Escalation to hotel staff
Guest interaction analytics
Deliverables

Create

business/

guest/

├── domain/
├── application/
├── infrastructure/
├── api/
├── services/
├── workflows/
├── concierge/
├── conversations/
├── preferences/
├── recommendations/
├── notifications/
├── events/
└── tests/
Specifications

Generate

.specs/business/guest/

guest-profile.md
guest-preferences.md
guest-conversation.md
concierge-agent.md
recommendation-engine.md
conversation-memory.md
service-discovery.md
guest-workflows.md
notifications.md
Documentation

Generate

docs/business/guest/

README.md
guest-profile.md
concierge.md
recommendations.md
conversation-memory.md
guest-workflows.md
api.md
Core Modules
Guest Profile

Manage

Guest identity
Contact information
Loyalty status
Stay history
Preferences
Favorite room types
Dietary restrictions
Accessibility requirements
Languages
Communication preferences

Guest profiles should evolve over time.

Guest Preference Engine

Learn and store

Room preferences
Pillow preferences
Food preferences
Check-in preferences
Service preferences
Favorite facilities
Frequently requested services

Preferences should influence future recommendations.

AI Concierge

Build the first public-facing AI assistant.

Responsibilities

Answer hotel FAQs
Explain hotel policies
Recommend facilities
Book services
Modify reservations (through Reservation Platform)
Suggest upgrades
Recommend restaurants
Recommend local attractions
Explain loyalty benefits

The concierge must never access databases directly.

It must communicate through:

Reservation Platform
AI Platform
Knowledge Platform
Agent Platform
Conversation Management

Support

Multi-turn conversations
Session history
Context retention
Conversation summarization
Conversation search
Conversation replay

Every conversation should have a unique ID.

Conversation Memory

Maintain

Short-term memory

Session memory

Guest profile memory

Preference memory

Long-term memory placeholder

Memory should expire according to configurable policies.

Recommendation Engine

Generate personalized recommendations for

Restaurants
Spa
Room upgrades
Hotel facilities
Events
Activities
Local attractions

Recommendations should combine

Guest profile
Preferences
Reservation context
Knowledge Platform
Business rules
Service Discovery

Allow guests to discover

Restaurants
Spa
Gym
Pool
Events
Nightlife
Transportation
Airport pickup
Meeting rooms

Results should include descriptions, availability, and eligibility.

Guest Workflows

Implement LangGraph workflows for

Ask Concierge
Request Room Service
Book Restaurant
Book Spa
Modify Reservation
Ask Hotel Policy
Request Late Checkout
Report Issue
Agent Design

Implement

Guest Concierge Agent

Responsibilities

Intent detection
Planning
Tool orchestration
Knowledge retrieval
Personalized responses
Escalation

The Concierge Agent should use

AI Platform
Agent Platform
Knowledge Platform
Reservation Platform
Tool Definitions

Create

SearchHotelKnowledgeTool

FindRestaurantTool

FindSpaServiceTool

RecommendFacilityTool

ReservationLookupTool

GuestPreferenceTool

EscalateToStaffTool

Every tool should declare

Input schema
Output schema
Permissions
Timeout
Retry policy
APIs

Implement

GET    /guests/{id}

PUT    /guests/{id}

GET    /guests/{id}/preferences

PUT    /guests/{id}/preferences

GET    /guests/{id}/recommendations

POST   /concierge/chat

GET    /conversations

GET    /conversations/{id}
Events

Publish

GuestProfileUpdated

PreferenceChanged

ConversationStarted

ConversationEnded

RecommendationGenerated

IssueReported

ServiceRequested

EscalationRequested

Notifications

Support

Internal notifications
Guest messages
Reservation reminders
Service confirmations
Recommendation notifications

Notification providers remain abstract.

Analytics

Track

Guest satisfaction proxy metrics
Concierge usage
Recommendation acceptance rate
Conversation length
Escalation frequency
Most requested services
Frequently asked questions
Average response latency
Security

The Guest Experience Platform must

Enforce RBAC
Validate guest identity
Protect conversation history
Mask sensitive information
Audit guest actions
Observability

Collect

Conversation latency
Tool execution time
Retrieval quality
Recommendation quality
AI token usage
Conversation success rate
Testing

Implement

Unit tests
Integration tests
Workflow tests
Agent tests
Prompt regression tests
Recommendation tests
API tests

Coverage target

≥95%

Quality Gates

Loop fails if

❌ Housekeeping module implemented

❌ Revenue forecasting implemented

❌ Dynamic pricing implemented

❌ Executive dashboard implemented

These belong to later loops.

Acceptance Criteria

The Guest Experience Platform should

Maintain guest profiles
Learn guest preferences
Provide personalized recommendations
Support natural conversations
Execute concierge workflows
Retrieve hotel knowledge
Integrate with reservations
Persist conversation history
Publish events
Pass all tests
Definition of Done

Loop 11 is complete only if

Guest Profile service operational
Preference engine implemented
AI Concierge operational
Recommendation engine functional
Conversation memory implemented
Guest workflows complete
APIs documented
Events published
Tests passing
Documentation complete
Exit Criteria

At the end of Loop 11, HospitalityAI delivers its first complete guest-facing experience.

A guest should be able to interact with the system conversationally, receive personalized assistance, access hotel knowledge, modify reservations through the Reservation Platform, and receive recommendations based on their profile and preferences.

Engineering Notes for Antigravity

Before implementation, Antigravity must:

Read the Constitution and execution-rules.md.
Review all previous loops, especially Loops 07–10.
Generate and obtain approval for the specifications under .specs/business/guest/.
Reuse existing AI Platform, Agent Platform, Knowledge Platform, and Reservation Platform components rather than introducing duplicate logic.
Implement features incrementally, ensuring every new component has corresponding tests, documentation, and observability.
Verify all quality gates before marking the loop complete.


Engineering Notes for Antigravity

Before implementation:

Read execution-rules.md and all previous loops.
Generate or update .specs/business/guest/ before writing code.
Reuse the AI Platform, Multi-Agent Platform, Knowledge Platform, and Reservation Platform—do not duplicate functionality.
Keep business logic inside the Guest domain; infrastructure concerns belong to earlier platform layers.
Use mock providers and deterministic test data where possible to keep tests repeatable.
Verify all quality gates, update documentation, and ensure CI passes before marking the loop complete.
Deliverables Summary

By the end of Loop 11, Antigravity should have produced:

business/guest/
.specs/business/guest/
docs/business/guest/

Guest Profile Service
Preference Learning Engine
AI Concierge Agent
Conversation Engine
Recommendation Engine
Itinerary Generator
Service Request Platform

REST APIs
LangGraph workflows
Tests
Documentation