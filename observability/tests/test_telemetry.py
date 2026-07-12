from typing import Any

import pytest

from observability.telemetry.logging import (
    add_correlation_id_processor,
    get_correlation_id,
    set_correlation_id,
)
from observability.telemetry.metrics import (
    get_or_create_counter,
    get_or_create_histogram,
    llm_calls_total,
    llm_cost_usd_total,
    llm_tokens_total,
    workflow_latency_seconds,
)
from observability.telemetry.tracing import start_trace_span


def test_correlation_id_propagation() -> None:
    # Initial get
    cid1 = get_correlation_id()
    assert cid1 != ""

    # Set new ID
    set_correlation_id("test-correlation-123")
    assert get_correlation_id() == "test-correlation-123"

    # Verify context injection processor
    event: dict[str, Any] = {}
    add_correlation_id_processor(None, "info", event)
    assert event["correlation_id"] == "test-correlation-123"


def test_metrics_registration() -> None:
    # Verify label names
    assert "model" in llm_calls_total._labelnames
    assert "type" in llm_tokens_total._labelnames
    assert "module" in llm_cost_usd_total._labelnames
    assert "workflow" in workflow_latency_seconds._labelnames

    # Duplicate registration should return existing metrics
    counter = get_or_create_counter(
        "llm_calls_total", "doc", ["model", "provider", "status"]
    )
    histogram = get_or_create_histogram("workflow_latency_seconds", "doc", ["workflow"])
    assert counter == llm_calls_total
    assert histogram == workflow_latency_seconds


def test_trace_span_context() -> None:
    # Verify starting span registers start/end traces
    with start_trace_span("test_workflow_node", {"target": "revenue"}) as span:
        assert span["span_name"] == "test_workflow_node"
        assert span["attributes"]["target"] == "revenue"

    # Verify exceptions are raised and logged
    with pytest.raises(ValueError):
        with start_trace_span("error_node"):
            raise ValueError("Failure in node execution")
