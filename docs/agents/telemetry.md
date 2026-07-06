# Agent Platform: Telemetry

This document details workflow traces monitoring and metrics aggregation.

## Traces Fields

The `AgentTelemetryTracker` logs `WorkflowTrace` snapshots:
- `thread_id`: Session thread key.
- `goal`: Target prompt.
- `duration_sec`: Latency speed in seconds.
- `tool_latencies`: Mapping of tool execution latency times.
- `retry_counts`: Steps retry numbers.
- `success`: Succeeded or failed.
- `failure_reason`: Error description.
- `execution_path`: Sequence list of nodes executed.
- `token_usage`: Mapped token counts from AI Platform.
