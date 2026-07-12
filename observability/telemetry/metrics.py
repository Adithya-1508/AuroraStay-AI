from prometheus_client import REGISTRY, Counter, Histogram


# Dynamic registry check helper to prevent duplicate metrics registration in test runs
def get_or_create_counter(
    name: str, documentation: str, labelnames: list[str]
) -> Counter:
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]  # type: ignore
    return Counter(name, documentation, labelnames)


def get_or_create_histogram(
    name: str, documentation: str, labelnames: list[str]
) -> Histogram:
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]  # type: ignore
    return Histogram(name, documentation, labelnames)


# Metric Definitions
llm_calls_total = get_or_create_counter(
    "llm_calls_total",
    "Total count of LLM inference requests",
    ["model", "provider", "status"],
)

llm_tokens_total = get_or_create_counter(
    "llm_tokens_total",
    "Total count of LLM tokens consumed",
    ["model", "type"],  # token_type: prompt vs completion
)

llm_cost_usd_total = get_or_create_counter(
    "llm_cost_usd_total",
    "Total estimated USD cost of AI operations",
    ["module"],
)

workflow_latency_seconds = get_or_create_histogram(
    "workflow_latency_seconds",
    "Latency of multi-agent and LangGraph workflows in seconds",
    ["workflow"],
)
