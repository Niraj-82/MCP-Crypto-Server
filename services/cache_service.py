import time

class Cache:
    def __init__(self):
        self._store = {}

    def get(self, key):
        """Retrieve a value from the cache.

        Args:
            key: Cache key string.

        Returns:
            The cached value if present and not expired, otherwise None.
        """
        entry = self._store.get(key)
        if entry and (entry['expires_at'] > time.time()):
            return entry['value']
        if key in self._store:
            del self._store[key]
        return None

    def set(self, key, value, ttl=30):
        """Set a value in the cache with a TTL (seconds).

        Args:
            key: Cache key string.
            value: Value to store.
            ttl: Time-to-live in seconds.
        """
        self._store[key] = {
            'value': value,
            'expires_at': time.time() + ttl,
        }

    def clear(self):
        """Clear all items from the cache."""
        self._store.clear()

cache = Cache()