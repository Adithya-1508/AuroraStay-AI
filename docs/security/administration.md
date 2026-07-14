# Enterprise Console & AI Governance

This module provides administrators with oversight of models, prompts, maintenance, and asset approvals.

## 1. System Maintenance Mode

- **Function**: Toggles the entire web service into static maintenance display.
- **Enforcement**: Blocks modifications, API writes, and query updates across business endpoints.

## 2. AI Model Approvals Register

- **Gatekeeping**: Blocks AI agents from executing forecasting/agentic logic unless the model ID is registered and marked as `"APPROVED"`.
- **States**: `PENDING`, `APPROVED`, `REJECTED`, `DEPRECATED`.

## 3. Prompt Template Approvals Register

- **Gatekeeping**: Prevents dynamic prompt expansions unless the template name is explicitly approved by the system administration console.
