# Product Risks and Mitigations

This document outlines key risks identified for the HospitalityAI platform, assessing likelihood and impact, and detailing mitigation strategies.

---

## 1. Risk Matrix

| Risk ID | Risk Description | Likelihood | Impact | Mitigation Strategy |
| --- | --- | --- | --- | --- |
| **R-101** | **LLM Hallucinations**: AI Concierge provides incorrect guest answers (e.g. telling a guest the pool is open 24 hours when it closes at 9 PM). | Medium | High | **Strict RAG Constraints**: Force the system to use system prompts that mandate answering *only* from retrieved chunks. Set LLM temperature to `0.0` for deterministic outputs. Implement automated post-processing validation checks. |
| **R-102** | **AI Booking Errors**: The reservation agent erroneously cancels or alters a reservation due to ambiguous guest input or parsing errors. | Low | High | **Two-Factor/Confirmation Gates**: Implement a strict verification step where the agent repeats the requested action (e.g. "I will cancel room 302 checking out July 10. Confirm?") and awaits explicit confirmation before executing database mutations. |
| **R-103** | **LLM Provider Outages / Latency spikes**: LLM provider API goes down or latency exceeds NFR limits, breaking guest chat. | Medium | Medium | **Fallback Routing / Offline Mocks**: Use client adapters that support automatic failovers to secondary LLM endpoints (e.g. fallback from Claude to Gemini). Expose offline prompt mocks returning simple answers for critical outages. |
| **R-104** | **Data Leakage (Security)**: A guest queries the AI Concierge and gets access to private data of other guests (names, room numbers). | Low | Critical | **Context Isolation**: Restrict the retrieval query contexts at the vector database search layer. Ensure the search query filters strictly on the current guest's identifier or public hotel FAQs. |
| **R-105** | **ML Forecast Drift**: Over time, occupancy prediction accuracies decrease due to shifting travel behaviors or seasonal fluctuations. | Medium | Medium | **Continuous Monitoring & Retraining**: Log mean absolute percentage errors (MAPEs) daily. Implement monthly automated model retraining schedules via MLflow. |
| **R-106** | **API Rate Limiting**: The platform exceeds the LLM provider rate limits (TPM/RPM) during busy booking hours. | Low | Medium | **Prompt Caching & Request Queues**: Enable prompt caching at the adapter layer. Implement throttling and request queues to prioritize reservation-related AI commands over generic FAQs. |
