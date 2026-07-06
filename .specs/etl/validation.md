# ETL Specification: Data Validation

Defines the validation framework checks, constraints, and failures handling.

## Validation Steps

1. **Schema check**:
   - Ensure all columns match the database schema types and structures.
2. **Null check**:
   - Assert that no mandatory fields contain null values (e.g. Guest email, Reservation check-in date).
3. **Duplicate check**:
   - Verify that primary keys and unique identifiers are unique within the ingestion batch.
4. **Referential Integrity**:
   - Confirm that linked records exist (e.g., Guest ID exists in database when loading Reservations).
5. **Business Ranges & Constraints**:
   - Check-out date must be greater than or equal to check-in date.
   - Total costs must be non-negative ($\ge 0$).
   - Review score must be integer between 1 and 5.

## Validation Failure Handling

- When validation failures occur, the validation engine must not crash silently.
- It must log all errors in a JSON Validation Report outlining:
  - Row number/ID with the error.
  - Column name.
  - Reason for failure.
  - Failed value.
- Mark `etl_executions.validation_status = 'FAILED'` if validation errors exceed critical thresholds (default $\gt 0$ critical errors).
