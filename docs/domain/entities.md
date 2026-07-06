# Domain Entities

This document defines the key business entities within the HospitalityAI platform, independent of database tables or ORM models.

---

## 1. Guest Entity
- **Purpose**: Represents an registered guest profile.
- **Identity**: `guest_id` (Unique UUID string).
- **Attributes**:
  - `first_name` (String)
  - `last_name` (String)
  - `email` (String, verified format)
  - `phone` (String, verified format)
  - `loyalty_tier` (LoyaltyTier Value Object)
  - `preferences` (GuestPreference Value Object)
- **Behavior**:
  - `upgrade_loyalty_tier(new_tier)`: Transitions guest to a higher tier.
  - `update_preferences(temp, pillow)`: Mutates preference attributes.
- **Validation Rules**:
  - Email must contain a valid `@` symbol.
- **Relationships**: One-to-many relationship with reservations.

---

## 2. Reservation Entity
- **Purpose**: Represents a contracted guest stay.
- **Identity**: `reservation_id` (Unique alphanumeric string).
- **Attributes**:
  - `guest_id` (Reference id)
  - `room_category_id` (Reference id)
  - `assigned_room_id` (Optional reference id)
  - `date_range` (DateRange Value Object)
  - `total_cost` (Money Value Object)
  - `status` (ReservationStatus)
- **Behavior**:
  - `assign_room(room_id)`: Assigns a room to the booking if room is clean.
  - `check_in()`: Transitions reservation state to CheckedIn.
  - `cancel()`: Transitions reservation state to Cancelled.
- **Validation Rules**:
  - Check-out date must succeed check-in date.
- **Relationships**:
  - Many-to-one with Guest.
  - Many-to-one with RoomCategory.
  - One-to-one with Room (optional).

---

## 3. Room Entity
- **Purpose**: Represents a specific guest room.
- **Identity**: `room_id` (Unique UUID).
- **Attributes**:
  - `room_number` (RoomNumber Value Object)
  - `category_id` (Reference id)
  - `status` (RoomStatus Value Object)
- **Behavior**:
  - `mark_dirty()`: Triggered at checkout.
  - `mark_clean()`: Triggered when housekeeping task completes.
  - `place_in_maintenance()`: Triggered on urgent repair requests.
- **Validation Rules**:
  - Room number must correspond to hotel building floor levels.
- **Relationships**: Many-to-one with RoomCategory.

---

## 4. HousekeepingTask Entity
- **Purpose**: Represents a room cleaning assignment.
- **Identity**: `task_id` (Unique UUID).
- **Attributes**:
  - `room_id` (Reference id)
  - `assigned_employee_id` (Optional reference id)
  - `status` (TaskStatus Value Object)
  - `created_at` (Timestamp)
  - `completed_at` (Optional timestamp)
- **Behavior**:
  - `assign_to(employee_id)`: Registers assignee and changes status to In Progress.
  - `complete()`: Changes status to Completed, logs timestamp, and triggers room clean status.
- **Validation Rules**:
  - `completed_at` must succeed `created_at`.
- **Relationships**: One-to-one with Room.
