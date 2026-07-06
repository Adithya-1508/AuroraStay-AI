# Spec: Conversations Domain Aggregate

- **Status**: Ready
- **Owner**: Knowledge Context Owner (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define chat sessions state machines, message attributes, and escalation triggers.

## 2. Responsibilities
- Hold conversation histories.
- Manage session statuses (Active, Staff-Controlled, Closed).
- Trigger receptionist handoff conditions.

## 3. Public Interfaces
```python
class Message:
    def __init__(self, sender: str, text: str, timestamp: datetime):
        self.sender = sender  # 'Guest', 'AI', or 'Staff'
        self.text = text
        self.timestamp = timestamp

class ChatSession:
    def __init__(self, session_id: str, guest_id: str):
        self.session_id = session_id
        self.guest_id = guest_id
        self.messages = []
        self.status = "Active"

    def add_message(self, message: Message) -> None:
        if self.status == "Closed":
            raise ValueError("Cannot add messages to a closed session.")
        self.messages.append(message)

    def escalate(self) -> None:
        self.status = "StaffControlled"

    def close(self) -> None:
        self.status = "Closed"
```

## 4. Invariants
- Closed sessions cannot be modified.
