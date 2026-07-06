# Business Rules and Invariants

This document specifies the logical rules, pricing strategies, and workflow sequencing constraints of HospitalityAI.

---

## 1. Reservation Overlap Rule
- **Description**: The system must check all active reservations for a specific room. No two bookings for the same room may overlap.
- **Reason**: Protects room capacity, preventing double booking failures.
- **Exception Cases**: Housekeeping reservations or room blocks (e.g. out of service for repair) are treated as active locks, preventing guest bookings.

---

## 2. Room Allocation Rule
- **Description**: Rooms may only be assigned to guests if the room status is `Clean` and its category matches the reservation Room Category.
- **Reason**: Ensures guests receive clean rooms of the category they booked.
- **Exception Cases**: Emergency overrides allow front desk staff to allocate a higher category room (e.g. Deluxe instead of standard) if standard rooms are dirty, without extra charge.

---

## 3. VIP Upgrade Recommendation Rule
- **Description**: When checking in a guest flagged as `VIP` (based on [LoyaltyTier](file:///c:/Users/adith/OneDrive/Desktop/Hospital-AI/docs/domain/value-objects.md#loyaltytier)), if a higher category room is vacant and clean, the system generates a room upgrade `Recommendation` for staff review.
- **Reason**: Elevates guest service quality while keeping humans in control of upgrades.
- **Exception Cases**: If the occupancy rate of the higher category is $\ge 90\%$, do not generate upgrade recommendations to preserve room availability for high-paying walk-ins.

---

## 4. Housekeeping Task Sequencing
- **Description**: Housekeeping tasks are prioritized based on incoming reservation arrivals. Rooms with expected check-ins for the day must be clean first.
- **Reason**: Minimizes guest waiting times during peak check-in hours.
- **Exception Cases**: VIP arrivals bypass standard queues, moving the assigned room task to the top of the queue.

---

## 5. Cancellation Penalty Rule
- **Description**: Guests can cancel reservations up to 24 hours before the check-in date without penalty. Cancellations within 24 hours incur a penalty fee equal to one night's stay.
- **Reason**: Protects hotel revenue from last-minute cancellations.
- **Exception Cases**: VIP loyalty members have fee waivers, permitting free cancellations at any time.
