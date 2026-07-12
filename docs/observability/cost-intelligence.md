# Cost Intelligence Manual

## Overview
Cost Intelligence tracks prompt and completion tokens consumed, multiplying them by provider pricing tiers to yield USD cost reports.

## Default Token Pricing Tiers (per 1K tokens)
- **gpt-4**: $0.03 input, $0.06 output.
- **claude-3-opus**: $0.015 input, $0.075 output.
- **gpt-3.5-turbo**: $0.0015 input, $0.0020 output.

## APIs
- **GET** `/api/v1/observability/cost`
  - Returns total cost metrics, breakdown by module, and caching/optimizations recommendations.
