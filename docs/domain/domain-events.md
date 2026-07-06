# Domain Events Catalog

This catalog outlines the domain events published inside the HospitalityAI Bounded Contexts.

---

## 1. `ReservationCreated`
- **Trigger**: A new reservation transaction is finalized and stored in the database.
- **Publisher**: Reservation Context (`ReservationService`)
- **Consumers**:
  - Guest Context: Updates guest stay history statistics.
  - Revenue Context: Feeds the occupancy forecast prediction pipeline.
- **Business Meaning**: Room inventory is locked, expected revenue is recorded, and loyalty check loops are queued.
- **Payload Schema**:
```json
{
  "reservation_id": "res_8877",
  "guest_id": "gst_1122",
  "room_category_id": "cat_deluxe",
  "date_range": {
    "start": "2026-07-10",
    "end": "2026-07-15"
  },
  "total_cost": {
    "amount": 750.00,
    "currency": "USD"
  }
}
```

---

## 2. `ReservationCancelled`
- **Trigger**: An active reservation is cancelled by the guest or receptionist.
- **Publisher**: Reservation Context (`ReservationService`)
- **Consumers**:
  - Revenue Context: Recalculates cancellation model probabilities.
  - Guest Context: Updates history logs.
- **Business Meaning**: Released room categories return to the availability pool.

---

## 3. `GuestCheckedIn`
- **Trigger**: A guest arrives, completes registration card checks, and receives keys.
- **Publisher**: Reservation Context (`Reservation` entity status change)
- **Consumers**:
  - Security Context: Registers active room access permissions keys.
- **Business Meaning**: Room state changes to `Occupied`.

---

## 4. `GuestCheckedOut`
- **Trigger**: A guest settles incident bills and leaves the room.
- **Publisher**: Reservation Context
- **Consumers**:
  - Operations Context: Generates room cleaning tasks in the housekeeping queue.
- **Business Meaning**: Room state changes to `Dirty`, and cleaning workers are notified.

---

## 5. `HousekeepingTaskCreated`
- **Trigger**: A guest checks out, generating a cleaning task.
- **Publisher**: Operations Context
- **Consumers**:
  - Dashboard Platform: Renders a new task in the housekeeper view.
- **Business Meaning**: Room turnaround queue begins.

---

## 6. `RecommendationGenerated`
- **Trigger**: ML forecasting or VIP check nodes detect rate changes or room upgrade opportunities.
- **Publisher**: Decision Intelligence Context
- **Consumers**:
  - Executive Dashboard: Triggers staff review notifications.
- **Business Meaning**: AI proposes a business optimization action.
