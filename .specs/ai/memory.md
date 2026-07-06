# AI Platform Specification: Memory Layer

## Overview
Declares interchangeable strategies to persist context, summaries, and long-term profiles across execution steps.

## Memory Types
1. **ConversationMemory**: Retains the immediate sequence of conversation steps.
2. **SessionMemory**: Stores transient variables and key-value states specific to the current session (e.g. current check-in date selection).
3. **WorkingMemory**: Stores immediate task context and planner goals.
4. **LongTermMemory (Placeholder)**: Defines boundaries to retrieve vector-indexed historical profiles (to be fully built in Loop 09).

## Interfaces
- `BaseMemory` interface declaring:
  - `store(key, value)`
  - `retrieve(key)`
  - `clear()`
