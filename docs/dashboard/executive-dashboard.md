# Executive Dashboard Manual

## Overview
The executive overview acts as a unified data aggregator. It calculates high-level metrics, executes the Alert Engine, compiles active widgets, and generates AI-recommended next steps.

## Key APIs
- **GET** `/api/v1/dashboard/executive`
  - **Permissions**: `Executive` or `General Manager` role required.
  - **Parameters**: None.
  - **Output**: JSON payload with `business_health_score`, `metrics`, `widgets`, `ai_recommendations`, and `alerts`.

## Business Health Score Formula
$$S = 30 \cdot \text{Occupancy} + 25 \cdot \text{ADR Score} + 20 \cdot \text{SLA Compliance} + 25 \cdot \text{Satisfaction} - 10 \cdot \text{Cancellations Today}$$
Calculated automatically out of 100 on every retrieval to provide immediate feedback on hotel operational state.
