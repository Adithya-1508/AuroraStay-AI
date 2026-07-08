# Guest Segmentation

The `GuestSegmenter` groups guest profiles into actionable marketing segments using a hybrid rule-based and machine-learning approach.

## Segmentation Mappings

### 1. VIP (Rule-based)
- **Criteria**: Guest has a loyalty tier of "Gold" or "Platinum".

### 2. Luxury Traveler (Rule-based)
- **Criteria**: Guest has spent more than \$1500.0 on past stays.

### 3. Business Traveler (Rule-based)
- **Criteria**: Guest has completed 5 or more stays.

### 4. Long Stay (Rule-based)
- **Criteria**: Guest has spent more than \$500.0 and has at least 2 stays.

### 5. Weekend Traveler (Default / KMeans fallback)
- **Criteria**: Guests not matching the above rule criteria are clustered using a 4-cluster K-Means model trained on stay frequency and total spending features.
