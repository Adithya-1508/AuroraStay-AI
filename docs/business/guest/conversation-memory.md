# Conversation Memory & Preference Learning

The **Preference Learning Engine** dynamically extracts guest choices from conversational text. This eliminates manual configuration, providing a seamless guest experience.

## Extractable Traits

1. **Room Layout**:
   - Matches keywords: `"king bed"`, `"king size"`, `"queen bed"`, `"high floor"`, `"upper floor"`, `"low floor"`.
2. **Pillow Preferences**:
   - Matches keywords: `"feather pillow"`, `"memory foam pillow"`, `"foam pillow"`.
3. **Dietary Restrictions**:
   - Matches keywords: `"vegetarian"`, `"vegan"`, `"gluten free"`, `"gluten-free"`.

## Architecture Diagram

```mermaid
sequenceDiagram
    participant Guest as Guest User
    participant Concierge as Concierge Service
    participant Memory as Preference Learning Engine
    participant DB as Postgres Database
    participant Events as Event Publisher

    Guest ->> Concierge: "I'd like a room with a king bed on a high floor, and please make sure food is vegetarian."
    Concierge ->> Memory: learn_preferences_from_text(guest_id, text)
    Memory ->> Memory: Extract traits (King bed, High floor, Vegetarian)
    Memory ->> DB: Update Guest.preferences JSONB
    Memory ->> Events: Publish PreferenceChanged Event
    Events -->> Guest: Event distributed (personalized updates ready)
```
