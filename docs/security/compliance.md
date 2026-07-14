# GDPR Purge & Data Privacy Compliance

This module enforces user data privacy, encrypts sensitive data, and complies with international regulations (GDPR).

## 1. Field-Level AES Encryption

- **Mechanism**: Encrypts sensitive columns (e.g., credit cards, contact phone numbers) before writing to the database using AES-256 (Fernet) keys.
- **Decryption**: Decrypts values dynamically upon retrieval for authorized roles.

## 2. GDPR Right to Delete

- **Anonymization mapping**:
  - `first_name` -> `"ANONYMIZED"`
  - `last_name` -> `"ANONYMIZED"`
  - `email` -> `"anonymized@gdpr.hospitalityai.local"`
  - `phone` -> `"ANONYMIZED"`
- **Metric Retention**: Preserves non-identifiable booking patterns, stay nights, and room revenue details for analytical reporting.
