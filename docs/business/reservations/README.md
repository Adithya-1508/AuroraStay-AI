# Intelligent Reservation Platform (Loop 10)

This documentation provides an architectural and functional overview of the Intelligent Reservation Platform implemented under `business/reservation/`.

---

## 1. Domain Entities & States

The reservation status flows through a strict state machine defined by `ReservationStatus`:

```mermaid
state_diagram
    [*] --> Confirmed : Place Booking
    Confirmed --> CheckedIn : Check-In
    Confirmed --> Cancelled : Cancel Booking
    CheckedIn --> CheckedOut : Check-Out
    CheckedOut --> [*]
```

### State Transitions
- **Place Booking**: Scans room category capacity. If vacancy exists, assigns a physical room (VIP prioritized) and sets status to `Confirmed`.
- **Check-In**: Locks the physical room status to `Occupied` and transitions reservation to `CheckedIn`.
- **Check-Out**: Clears reservation room assignment, releases the room setting its status to `Dirty` for housekeeping, and transitions reservation to `CheckedOut`.
- **Cancellation**: Processes cancellation, calculating refund penalties according to policies, and releases the assigned room.

---

## 2. Dynamic Pricing Engine

Stay rates are calculated dynamically based on base category pricing, seasonal multipliers, weekend surcharges, promo codes, and loyalty discounts:

$$Total = (Base \times SeasonalMultiplier \times WeekendMultiplier - LoyaltyDiscount - PromoDiscount) \times 1.12_{tax}$$

### Multipliers
- **Seasonal Rates**:
  - Summer Peak (June 1 – August 31): **1.3x**
  - Holiday Peak (December 15 – January 5): **1.5x**
- **Weekend Surcharge**: Friday and Saturday nights receive a **1.15x** markup.
- **Loyalty Discounts**:
  - Platinum: **15%**
  - Gold: **10%**
  - Silver: **5%**
  - Bronze / None: **0%**

---

## 3. VIP Priority Allocation & Upgrades

During booking placement:
1. If a room of the requested category is available, it is assigned.
2. If the category is sold out, guests with higher loyalty tiers (Platinum or Gold) are automatically considered for upgrade recommendations to the next available category.
3. Priority room allocation selects the best available physical rooms first (e.g., lower index or specific preferences).

---

## 4. Decoupled Notifications

Events emit structured payloads handled by the Notification Service:
- **Reservation Confirmation**: Sent immediately upon booking.
- **Reservation Reminder**: Triggered before check-in.
- **Reservation Modification / Cancellation**: Sends updated logs.

The service uses a decoupled adapter design, permitting future integrations of real SMS/Email providers (e.g., Twilio, SendGrid) without editing business service code.

---

## 5. LangGraph Conversational Agent

The platform embeds a `ReservationAssistantAgent` powered by the AI Platform and LangGraph:

- **State Graph Nodes**: Planner -> Tool Executor -> Human Approval Gate -> Supervisor.
- **Approval Gate**: Intercepts modifications, cancellations, and booking confirmations to request user approval.
- **Tools**:
  - `SearchAvailabilityTool`
  - `CalculatePriceTool`
  - `ReserveRoomTool`
  - `ModifyReservationTool`
  - `CancelReservationTool`
  - `RecommendUpgradeTool`
