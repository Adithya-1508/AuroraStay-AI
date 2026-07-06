# AI Platform Specification: Structured Outputs

## Overview
Enforces strict JSON formatting, type validation, and error self-correction.

## Validation Pipeline
1. Input: Request details alongside a target Pydantic Model or JSON Schema.
2. Formats: Instruct the LLM to write replies structured as JSON matching the schema.
3. Parsing: Parse raw response string to target dictionary/Pydantic object.
4. Corrective Retries: On parsing or schema validation error:
   - Resubmit raw response and exception details back to the LLM.
   - Instruct the LLM to fix the formatting.
   - Repeat up to 2 times before raising `StructuredParsingError`.
