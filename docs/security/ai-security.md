# AI Guardrails & Secrets Protection

This module protects the system from prompt-based vulnerabilities and protects environment credentials.

## 1. Sliding Window Rate Limiter

- **Mechanism**: Stores request timestamps per client IP.
- **Enforcement**: Drops requests exceeding maximum window thresholds (e.g., 100 requests per 60 seconds) to prevent DDoS and API resource exhaustion.

## 2. Prompt Injection Scanners

- **Heuristic Pattern Matching**: Scans user prompt strings for behavioral override injection markers:
  - `ignore previous instructions`
  - `bypass safety guidelines`
  - `system prompt disclosure`
- **Containment Action**: Automatically drops the request and flags the client session as critical risk.

## 3. Output Leakage Guardrails

- **Groundedness Scanners**: Analyzes LLM responses to verify system prompt constraints.
- **Pattern Matching**: Blocks outputs containing prompt templates or system configuration instructions.

## 4. Log Secrets Masking

- **Sanitization**: Intercepts configuration values and sensitive environment keys.
- **Masking Rules**: Replaces secret characters with masked strings (`db_p..._123`) to prevent accidental logs leakage.
