# User Stories

This document defines the key user stories for HospitalityAI, indicating priority, business value, and specific acceptance criteria.

---

## 1. Guest Stories

### US-101: Conversational FAQ Retrieval
- **As a** Guest,
- **I want to** ask questions about hotel services (like pool hours, checkout times, gym rules) in natural language,
- **So that** I can get instant answers without calling the front desk.
- **Priority**: High
- **Business Value**: Eliminates up to 60% of routine phone calls, freeing up receptionist time.
- **Acceptance Criteria**:
  - [ ] System answers within 1.5 seconds.
  - [ ] System uses a Vector database (RAG) to ensure answers are based on official hotel data.
  - [ ] If the question is outside the hotel's data, the agent politely states it cannot help and offers front-desk handoff.

### US-102: Conversational Room Booking
- **As a** Guest,
- **I want to** request a room booking via chat by stating my dates and room preference (e.g. "reserve a Deluxe Room for next weekend"),
- **So that** I can complete a reservation without filling out a traditional multi-step web form.
- **Priority**: High
- **Business Value**: Increases booking conversions through low-friction conversational commerce.
- **Acceptance Criteria**:
  - [ ] Agent parses dates and room types correctly using entity recognition.
  - [ ] System checks database availability and responds with options and pricing.
  - [ ] System reserves the room and returns a mock confirmation ID.

---

## 2. Front Desk Stories

### US-201: Reservation Management Interface
- **As a** receptionist,
- **I want to** view, create, edit, and cancel room reservations from a central portal,
- **So that** I can assist walk-in guests and handle phone modifications.
- **Priority**: High
- **Business Value**: Enables baseline operations for front desk managers.
- **Acceptance Criteria**:
  - [ ] Receptionists can search reservations by guest name or confirmation ID.
  - [ ] Changing a booking date checks room type availability and recalculates rate.
  - [ ] System locks rooms on booking to prevent double bookings.

---

## 3. Revenue Manager Stories

### US-301: Demand & Occupancy Forecasting
- **As a** Revenue Manager,
- **I want to** view an occupancy forecast for the next 30 days based on historical booking trends,
- **So that** I can adjust room pricing categories to maximize revenue.
- **Priority**: High
- **Business Value**: Boosts RevPAR (Revenue Per Available Room) by 5% to 15% through proactive dynamic pricing.
- **Acceptance Criteria**:
  - [ ] System displays occupancy forecast as a daily line chart.
  - [ ] System logs historical error rates (MAPEs) for the prediction model.

### US-302: Booking Cancellation Risks
- **As a** Revenue Manager,
- **I want to** see cancellation risk scores on each reservation,
- **So that** I can manage overbooking limits without risking walks.
- **Priority**: Medium
- **Business Value**: Minimizes lost revenue from last-minute cancellations.
- **Acceptance Criteria**:
  - [ ] System classifies each active reservation with a risk probability (High, Medium, Low).
  - [ ] Displays key risk indicators (e.g., booked via OTA, no deposit, short booking window).

---

## 4. Operations Manager Stories

### US-401: Automated Housekeeping Tasks
- **As an** Operations Manager,
- **I want** the system to automatically generate cleaning tasks for housekeeping when a guest checks out,
- **So that** rooms are cleaned and prepared for incoming arrivals as quickly as possible.
- **Priority**: High
- **Business Value**: Decreases room turnaround times, enabling earlier check-ins.
- **Acceptance Criteria**:
  - [ ] Checking out a reservation creates a task in the Housekeeping backlog.
  - [ ] Housekeeping status changes (Dirty -> In Progress -> Clean) update room availability immediately.
