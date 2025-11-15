import pytest
from services.cache_service import cache

def test_set_and_get_cache():
    cache.clear()
    cache.set("foo", {"a": 1}, ttl=2)
    assert cache.get("foo") == {"a": 1}

def test_cache_expiry():
    cache.clear()
    cache.set("bar", 123, ttl=1)
    import time
    time.sleep(2)
    assert cache.get("bar") is None