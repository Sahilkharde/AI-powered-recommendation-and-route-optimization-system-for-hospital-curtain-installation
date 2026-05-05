"""
In-memory cache layer with TTL support.

Designed as a drop-in that works without Redis for development/testing.
When Redis is available, swap the backend by setting REDIS_URL in config.
The API surface stays identical either way.
"""

import json
import time
import threading
from typing import Any


class TTLCache:
    """Thread-safe in-memory cache with per-key TTL expiration."""

    def __init__(self, default_ttl: int = 300):
        self._store: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()
        self._default_ttl = default_ttl

    def get(self, key: str) -> Any | None:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expires_at = entry
            if time.time() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        ttl = ttl if ttl is not None else self._default_ttl
        with self._lock:
            self._store[key] = (value, time.time() + ttl)

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._store.pop(key, None) is not None

    def invalidate_prefix(self, prefix: str) -> int:
        """Remove all keys starting with the given prefix."""
        with self._lock:
            keys = [k for k in self._store if k.startswith(prefix)]
            for k in keys:
                del self._store[k]
            return len(keys)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    def stats(self) -> dict:
        with self._lock:
            now = time.time()
            total = len(self._store)
            expired = sum(1 for _, (__, exp) in self._store.items() if now > exp)
            return {"total_keys": total, "expired_pending_cleanup": expired, "active": total - expired}


try:
    import redis as _redis_lib

    class RedisCache:
        """Redis-backed cache. Same interface as TTLCache."""

        def __init__(self, url: str = "redis://localhost:6379/0", default_ttl: int = 300):
            self._client = _redis_lib.from_url(url, decode_responses=True)
            self._default_ttl = default_ttl

        def get(self, key: str) -> Any | None:
            raw = self._client.get(key)
            if raw is None:
                return None
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                return raw

        def set(self, key: str, value: Any, ttl: int | None = None) -> None:
            ttl = ttl if ttl is not None else self._default_ttl
            self._client.setex(key, ttl, json.dumps(value, default=str))

        def delete(self, key: str) -> bool:
            return self._client.delete(key) > 0

        def invalidate_prefix(self, prefix: str) -> int:
            keys = list(self._client.scan_iter(match=f"{prefix}*", count=500))
            if keys:
                return self._client.delete(*keys)
            return 0

        def clear(self) -> None:
            self._client.flushdb()

        def stats(self) -> dict:
            info = self._client.info("keyspace")
            db_info = info.get("db0", {})
            return {"total_keys": db_info.get("keys", 0), "backend": "redis"}

except ImportError:
    RedisCache = None  # type: ignore[assignment, misc]


def create_cache(redis_url: str | None = None, default_ttl: int = 300):
    """
    Factory: returns RedisCache if redis_url is provided and the redis
    package is installed, otherwise falls back to TTLCache.
    """
    if redis_url and RedisCache is not None:
        try:
            cache = RedisCache(url=redis_url, default_ttl=default_ttl)
            cache.get("__ping__")
            return cache
        except Exception:
            pass
    return TTLCache(default_ttl=default_ttl)


# ── Cache key builders ───────────────────────────────────────────────────────

RECOMMEND_TTL = 120   # recommendations valid for 2 minutes
TRACK_COUNT_TTL = 60  # track install counts valid for 1 minute


def recommendation_key(curtain_barcode: str) -> str:
    return f"rec:{curtain_barcode}"


def track_counts_key(hospital_id: int) -> str:
    return f"track_counts:{hospital_id}"


def match_curtains_key(track_barcode: str) -> str:
    return f"match:{track_barcode}"


def route_key(installer_id: int, date_str: str) -> str:
    return f"route:{installer_id}:{date_str}"
