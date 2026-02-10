"""Cache service - entirely dead code (never imported anywhere)."""

from typing import Any, Optional
import time


class CacheService:
    """In-memory cache. NEVER USED - this entire file is dead code."""

    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self._cache = {}
        self._timestamps = {}

    def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        if key not in self._cache:
            return None

        # Check expiration
        if time.time() - self._timestamps[key] > self.ttl:
            del self._cache[key]
            del self._timestamps[key]
            return None

        return self._cache[key]

    def set(self, key: str, value: Any):
        """Set cached value."""
        self._cache[key] = value
        self._timestamps[key] = time.time()

    def delete(self, key: str):
        """Delete cached value."""
        self._cache.pop(key, None)
        self._timestamps.pop(key, None)

    def clear(self):
        """Clear all cached values."""
        self._cache = {}
        self._timestamps = {}


# Global cache instance - never used
_cache = None


def get_cache() -> CacheService:
    """Get global cache instance."""
    global _cache
    if _cache is None:
        _cache = CacheService()
    return _cache


def cached(ttl: int = 3600):
    """Decorator for caching function results. Never used."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = get_cache()
            key = f"{func.__name__}:{args}:{kwargs}"
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result)
            return result
        return wrapper
    return decorator
