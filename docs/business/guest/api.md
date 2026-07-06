# API Reference

The Guest Experience Platform registers several REST endpoints under the `/guests` and `/concierge` routing groups.

## Endpoints Summary

### Guest CRM Routes
* **POST `/guests`**
  Creates a new guest profile.
  - Body: `GuestProfileCreate`
  - Returns: Guest profile summary.
* **GET `/guests/{id}`**
  Retrieves a guest profile.
  - Returns: Guest details.
* **PUT `/guests/{id}`**
  Modifies fields on a guest profile.
  - Body: `GuestProfileUpdate`

### Preferences & Recommendations
* **GET `/guests/{id}/preferences`**
  Retrieves learned preferences.
* **PUT `/guests/{id}/preferences`**
  Saves preferences explicitly.
  - Body: `PreferenceSetUpdate`
* **GET `/guests/{id}/recommendations`**
  Generates guest recommendations.

### AI Concierge Routes
* **POST `/concierge/chat`**
  Processes chat queries through the concierge service.
  - Body: `ConciergeChatRequest`
  - Returns: Chat response, citations, and actions.
* **GET `/conversations`**
  Lists all active conversation sessions.
* **GET `/conversations/{id}`**
  Retrieves message timeline of a conversation session.
