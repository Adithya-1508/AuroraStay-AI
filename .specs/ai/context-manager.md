# AI Platform Specification: Context Management

## Overview
Coordinates token auditing, history caching, and window safety controls to prevent LLM context overflows.

## Mapped Structures
- `ConversationContext`: Holds lists of current messages, metadata injections, and limits.
- `TokenBudgeter`: Calculates token counts utilizing tiktoken or basic characters-to-tokens approximations.
- `ContextTrimmer`:
  - Mapped maximum context limit.
  - Trim policies: When messages token sum exceeds the limit, systematically trim the oldest non-system messages while keeping the system prompt intact.
  - Support context summarization triggers (delegated to later loops).
