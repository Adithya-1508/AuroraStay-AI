# Ubiquitous Language Mapping & Grammar Rules

This document establishes the mappings between the business glossary and the technical domains (code symbols, database tables, API routes, and system prompts) to prevent terminology conflicts.

---

## 1. Domain Object Translation Map

| Business Glossary Term | Code Class Name | API Endpoint | Database Table | LLM Prompt Variable |
| --- | --- | --- | --- | --- |
| **Guest** | `Guest` | `/api/v1/guests/` | `guests` | `guest_name`, `guest_id` |
| **Reservation** | `Reservation` | `/api/v1/reservations/` | `reservations` | `reservation_details` |
| **Room** | `Room` | `/api/v1/rooms/` | `rooms` | `room_number` |
| **Room Category** | `RoomCategory` | `/api/v1/room-categories/` | `room_categories` | `room_category_name` |
| **Task** | `HousekeepingTask` | `/api/v1/housekeeping/tasks` | `housekeeping_tasks` | `task_status` |
| **Conversation** | `ChatSession` | `/api/v1/chat/sessions` | `chat_sessions` | `session_history` |

---

## 2. Grammar Rules for AI Prompts
To maintain consistency and block hallucinations, all AI system prompts must adhere to the following rules:
- **Refer to the Customer as "Guest"**: Never use "user", "client", or "customer" in prompts. System instructions should state: *"You are assisting the Guest."*
- **Room Selections must use "Room Category"**: Never prompt the LLM to ask for a "room type" or "room tier". The instructions should refer to selecting a *Room Category*.
- **Use "Handoff to Staff"**: When the agent cannot solve a request, use the phrase *"escalating the guest request to staff"* rather than "transferring to human agent" or "notifying support".

---

## 3. Code Symbol Conventions
- **No Booking Class**: While "booking" is acceptable in guest-facing text, the backend code must exclusively use the word `Reservation` (e.g. `ReservationService`, `ReservationRepository`).
- **No Job Class**: Do not name operational cleaning structures "Job". Use `HousekeepingTask` or `MaintenanceRequest`.
