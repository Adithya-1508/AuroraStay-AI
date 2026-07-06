# Data Platform: Feature Store Registry Foundation

This document details the metadata feature tracking parameters.

## Core Concepts

The Feature Store registry maps features target definitions to track ML variables versioning before operational ML models are trained.

## Registered Feature Definitions

1. **`guest_stay_frequency`**:
   - **Owner**: Loyalty Engineering Team
   - **Version**: 1.0.0
   - **Description**: Tracks historical reservation booking counts for guests.
   - **Dependencies**: `reservations.id` count.
   - **Source Dataset**: `reservations` table.
   - **Refresh Schedule**: Daily.

2. **`guest_total_spend`**:
   - **Owner**: Revenue Management Team
   - **Version**: 1.0.0
   - **Description**: Calculates cumulative payment spend across all bookings.
   - **Dependencies**: `reservations.total_cost` sum.
   - **Source Dataset**: `reservations` table.
   - **Refresh Schedule**: Daily.
