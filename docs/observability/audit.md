# Audit Platform Manual

## Overview
The Audit Platform traces prompt executions, agent decisions, and workflow steps.

## Log Telemetry & Context Propagation
1. **Correlation IDs**: Request context correlation IDs are managed dynamically using a Python `contextvars.ContextVar`.
2. **Logging Processor**: A `structlog` processor automatically injects `correlation_id` into every JSON output.
3. **Trace Spans**: Node execution bounds are wrapped in `start_trace_span` context managers, logging start, exit latency, and exceptions.
