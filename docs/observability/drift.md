# Drift Detection Manual

## Overview
Drift Detection computes shifts between historical and current feature/target distributions, raising alerts when statistics exceed configured parameters.

## Mathematical Formulation
- **Population Stability Index (PSI)**: Measures structural shift over historical and current prediction distributions.
- **Alert Levels**:
  - `Warning`: PSI score exceeds `0.25`.
  - `Critical`: Features feature drift score exceeds `0.25`.

## API Endpoint
- **GET** `/api/v1/observability/drift`
  - Computes and returns the drift score and raises alerts.
