# Product Assumptions

This document lists the underlying assumptions on which the HospitalityAI requirements are based.

---

## 1. Mock Integration Boundaries

- **Property Management System (PMS)**: We assume that the platform does not need to connect to a real, commercial legacy PMS (such as Opera or Sabre) for this scope. All database persistence is handled inside the repository's database schema.
- **Payment Gateway**: We assume that payment processing (e.g. Stripe, PayPal) is out of scope. The reservation engine will assume payment is successful upon receiving dummy card details.
- **Messaging Channels**: We assume the guest-facing AI Concierge will run inside a mock web-chat widget on the hotel dashboard, rather than directly integrating with real-world WhatsApp, SMS, or WeChat numbers (which require developer business verification).

---

## 2. Data and Operations

- **Single Hotel Scope**: The platform assumes it is deployed for a single luxury hotel instance. Multi-tenancy (managing multiple separate hotel properties under one dashboard account) is out of scope.
- **Historical Stay Data**: We assume historical booking, occupancy, and guest review data are available in structured formats (CSV files or database seeds) to train the occupancy forecast models and seed the search databases.
- **Language**: The initial version of the AI Concierge and dashboard assumes English is the primary language. Multilingual support is deferred to future releases.

---

## 3. Platform Runtime

- **LLM Availability**: We assume continuous access to cloud-based LLM APIs (Gemini, Claude, or OpenAI). The system assumes these services maintain $\ge 99\%$ uptime.
- **Static Assets**: We assume all hotel policy guides, menu PDF documents, and facility hours lists are available as static files to populate the RAG Vector database.
