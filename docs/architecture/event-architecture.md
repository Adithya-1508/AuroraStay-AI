# Event-Driven Architecture

HospitalityAI leverages Redis Pub/Sub for loose decoupling of operations, analytical data streams, and background tasks.

## 1. Event Message Flow

```
   ┌───────────────────────┐
   │    Event Producer     │ (e.g. Reservation Service Checkout)
   └───────────┬───────────┘
               │ Publish JSON Event
   ┌───────────▼───────────┐
   │    Redis Pub/Sub      │ (Channel: 'hotel_events')
   └───────────┬───────────┘
               ├──────────────────────────┐ Dispatch to Subscribers
   ┌───────────▼───────────┐   ┌──────────▼───────────┐
   │ Housekeeping Task     │   │ Analytics Sentiment  │
   │ Subscriber            │   │ Subscriber           │
   └───────────────────────┘   └──────────────────────┘
```

---

## 2. Platform Event Catalog

### Event 1: `reservation.checkout`
- **Trigger**: A guest checked out at the front desk or via self-service chat.
- **Payload Schema**:
```json
{
  "event_id": "evt_987654321",
  "event_type": "reservation.checkout",
  "timestamp": "2026-07-04T16:00:00Z",
  "data": {
    "reservation_id": "res_12345",
    "room_id": "rm_302",
    "guest_id": "gst_9988"
  }
}
```
- **Consumer**: *Housekeeping Service* listens to this event to automatically create a room cleaning task.

### Event 2: `housekeeping.status_updated`
- **Trigger**: A housekeeper marked a room as cleaned.
- **Payload Schema**:
```json
{
  "event_id": "evt_11223344",
  "event_type": "housekeeping.status_updated",
  "timestamp": "2026-07-04T16:30:00Z",
  "data": {
    "room_id": "rm_302",
    "status": "Clean",
    "updated_by": "emp_054"
  }
}
```
- **Consumer**: *Reservation Engine* listens to this event to update the available room pool.

### Event 3: `review.received`
- **Trigger**: A guest submitted review comments.
- **Payload Schema**:
```json
{
  "event_id": "evt_55667788",
  "event_type": "review.received",
  "timestamp": "2026-07-04T16:45:00Z",
  "data": {
    "review_id": "rev_3322",
    "guest_id": "gst_9988",
    "review_text": "Had a fantastic stay, but the gym hours were too short."
  }
}
```
- **Consumer**: *ML Pipeline* analyzes the review text for sentiment and triggers alarms if negative sentiments contain operational issues.
