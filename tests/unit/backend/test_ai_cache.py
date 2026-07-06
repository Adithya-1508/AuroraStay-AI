from backend.ai.cache.semantic import AICache


def test_ai_cache_exact_matching() -> None:
    """Verifies that cache set/get operations match prompt messages hash signatures."""
    cache = AICache()
    messages = [{"role": "user", "content": "hello"}]

    assert cache.get(messages, "model-x", "provider-y") is None

    cache.set(messages, "model-x", "provider-y", "Cached Response content")
    assert cache.get(messages, "model-x", "provider-y") == "Cached Response content"

    # Different model should miss cache
    assert cache.get(messages, "model-other", "provider-y") is None


def test_ai_cache_ttl_expiration() -> None:
    """Verifies that cache entries expire according to TTL boundaries."""
    cache = AICache()
    messages = [{"role": "user", "content": "hello"}]

    # Set cache with negative TTL to simulate immediate expiration
    cache.set(messages, "model-x", "provider-y", "Expired Content", ttl=-1.0)
    assert cache.get(messages, "model-x", "provider-y") is None
