# Alert Engine Manual

## Overview
The Alert Engine validates platform metrics against operational parameters, automatically triggering warnings or critical alerts with severity levels, reasons, owners, and suggested actions.

## Operational Thresholds
- **Low Occupancy**: Average 7-day occupancy forecast < 40%.
- **Revenue Drop**: Daily revenue drops > 20% compared to 7-day average.
- **High Cancellations**: Day bookings cancellation count > 5.
- **Maintenance Backlog**: Critical maintenance tasks unassigned.
- **SLA Violations**: Room turnaround compliance < 90%.
- **Poor Guest Satisfaction**: Average sentiment rating < 3.5.
- **Model Drift**: Forecasting drift score > 0.25.
- **Knowledge Failures**: RAG query confidence < 0.30.

## API
- **GET** `/api/v1/dashboard/alerts`: Retrieve list of active warnings.
