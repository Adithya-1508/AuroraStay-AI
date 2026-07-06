# Spec: Operations & Revenue Analytics

- **Status**: Ready
- **Owner**: Data Platform Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the business calculations and schemas for generating key hotel performance indicators (Occupancy Rate, ADR, RevPAR) and housekeeping performance statistics.

## 2. Responsibilities
- Aggregate active stays, available inventory, and room prices to calculate occupancy levels.
- Apply standard revenue formulas:
  - **Occupancy Rate**: $\frac{\text{Rooms Booked}}{\text{Total Rooms Available}} \times 100$
  - **Average Daily Rate (ADR)**: $\frac{\text{Total Room Revenue}}{\text{Rooms Booked}}$
  - **RevPAR (Revenue Per Available Room)**: $\text{Occupancy Rate} \times \text{ADR} = \frac{\text{Total Room Revenue}}{\text{Total Rooms Available}}$
- Measure cleaning durations for housekeeping operations (Task completion time minus start time).
- Provide historical timelines for comparative revenue reporting.

## 3. Dependencies
- **Data Platform**: To query bookings, rooms, and task states.
- **ML Platform**: To fetch occupancy predictions for timeline visualizations.

## 4. Interfaces
```python
# Conceptual interfaces for Analytics Service

class AnalyticsService:
    async def get_occupancy_kpis(
        self, start_date: date, end_date: date
    ) -> OccupancyKPIsSchema:
        """Calculates historical and pacing occupancy percentages."""
        pass

    async def get_revenue_kpis(
        self, start_date: date, end_date: date
    ) -> RevenueKPIsSchema:
        """Calculates total room revenue, ADR, and RevPAR."""
        pass

    async def get_housekeeping_efficiency(
        self, start_date: date, end_date: date
    ) -> List[HousekeeperMetricSchema]:
        """Aggregates housekeeper completion speeds and task volumes."""
        pass
```

## 5. Configuration
- `EXCLUDED_ROOM_TYPES`: List of room types (e.g. staff rooms) excluded from inventory availability denominators.
- `TARGET_REVPAR`: Monthly performance threshold triggers for dashboard indicators.

## 6. Error Handling
- `ZeroRoomsAvailableError`: Handled gracefully during calculations to prevent division-by-zero errors.
- `AnalyticsDateRangeError`: Raised when the query duration range exceeds maximum limits (e.g. $\ge 12\text{ months}$).

## 7. Security
- Only users with the roles `Manager` or `Admin` can query revenue and housekeeper performance metrics.
- Enforce parameterized date inputs to block path or database vulnerabilities.

## 8. Testing
- **Unit Tests**:
  - Assert core formulas evaluate correctly under various booking configurations.
  - Test calculation outputs with zero active bookings.
- **Integration Tests**:
  - Verify database aggregation performance when processing historical reservation tables.

## 9. Acceptance Criteria
- [ ] Correctly calculates RevPAR and ADR metrics based on active bookings.
- [ ] Correctly filters out out-of-service/maintenance rooms from occupancy rates.
- [ ] Returns structured JSON schemas compatible with standard charting tools.
