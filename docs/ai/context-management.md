# AI Platform: Context Management

This document details history context building, token budgeting, and window overflow preventions.

## Token Estimations

A lightweight character-count estimator approximates message token usage:
$$\text{Tokens} \approx \frac{\text{Length of String}}{4}$$

## History Trimming Algorithm

When adding messages:
1. Estimate total tokens.
2. If token sum exceeds context limits (e.g. `max_tokens=4000`):
   - Loop and pop the oldest non-system message.
   - Keep the system prompt intact.
   - Re-check token budget.
3. Exposes clean message lists to providers.
