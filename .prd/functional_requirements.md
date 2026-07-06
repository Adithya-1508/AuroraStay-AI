# Functional Requirements

This document outlines the detailed functional requirements of the HospitalityAI platform, categorized by system components.

---

## 1. Reservation Engine (RE)

The platform must support core reservation processing:
- **FR-101: Availability Search**: The system must allow users to query room availability by room type, check-in date, and check-out date.
- **FR-102: Create Booking**: The system must support creating reservations with Guest details, Room type, stay dates, and a calculated rate, generating a unique booking confirmation ID.
- **FR-103: Modify Booking**: Staff and authorized users must be able to change stay dates, guest counts, and room types on active reservations, checking for capacity constraints.
- **FR-104: Cancel Booking**: The system must support cancellation of bookings, releasing the associated room inventory back to availability.

---

## 2. AI Concierge (AC)

The platform must support conversational AI capabilities:
- **FR-201: Natural Language Processing**: The system must interpret user inquiries in natural language, extracting intents and entities (e.g. check-in dates, room options).
- **FR-202: Knowledge Base Q&A (RAG)**: The system must use Retrieval-Augmented Generation to answer guest questions based solely on verified hotel information documents.
- **FR-203: Automated Actions**: The AI Concierge must be able to call tools (e.g. search availability, check reservation status) on behalf of the user when requested.
- **FR-204: Staff Handoff**: The system must support handing off the chat session to front desk staff when queries are unsupported, high-priority complaints, or when requested explicitly.

---

## 3. Operations & Analytics Dashboard (AD)

The system must visualize metrics and KPIs for staff:
- **FR-301: Real-time Occupancy**: Display current occupancy rate (Percentage of clean, booked rooms vs total rooms).
- **FR-302: Revenue KPIs**: Display total daily/weekly revenue, Average Daily Rate (ADR), and RevPAR.
- **FR-303: Housekeeping Tracker**: List housekeeping tasks categorized by status (Pending, In Progress, Clean) with completion times.
- **FR-304: Forecast Charts**: Render occupancy pacing and revenue forecasts.
- **FR-305: Reviews Sentiment**: Display aggregated guest review sentiment scores.

---

## 4. Machine Learning Platform (ML)

The platform must run inference for predictive modeling:
- **FR-401: Occupancy Forecasting**: Predict daily occupancy percentage for the next 30 days based on historical stay patterns and calendar events.
- **FR-402: Cancellation Classifier**: Predict cancellation risk (probability 0-1) for every active reservation.
- **FR-403: Upgrade Recommender**: Rank and suggest room upgrades (e.g. Deluxe, Suite) for existing bookings based on historical conversion trends.
- **FR-404: Sentiment Analyzer**: Classify incoming guest reviews into Positive, Neutral, or Negative sentiment categories.
