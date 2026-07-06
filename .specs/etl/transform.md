# ETL Specification: Data Transformation

Defines cleaning, normalization, and transformation rules for ingested datasets.

## Core Transformers

1. **Cleaning Rules**:
   - Null default resolution (e.g. converting null loyalty tiers to "Bronze").
   - Strip whitespace from all string columns.
   - Force date formatting to ISO format (`YYYY-MM-DD`).
2. **Normalization Rules**:
   - Phone numbers: Convert to E.164 formats where valid (e.g., `+1-555-0199`).
   - Emails: Enforce lowercase conversion.
   - Currency/Money: Convert all decimal representations to standard floats/decimals.
3. **Deduplication Rules**:
   - Guests: Deduplicate by lowercase `email` field.
   - Reservations: Deduplicate by unique primary reservation codes.
4. **Feature Engineering Hook**:
   - Pre-calculates base attributes (e.g., Guest tenure days based on first check-in, total historical stays) to prepare dataset inputs for future feature store registrations.
