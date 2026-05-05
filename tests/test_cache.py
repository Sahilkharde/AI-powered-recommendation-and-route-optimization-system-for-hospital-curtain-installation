"""Tests for the TTL cache layer."""

import time
import unittest

from app.cache import TTLCache, create_cache


class TestTTLCache(unittest.TestCase):
    def setUp(self):
        self.cache = TTLCache(default_ttl=5)

    def test_set_and_get(self):
        self.cache.set("k1", {"data": 42})
        self.assertEqual(self.cache.get("k1"), {"data": 42})

    def test_get_missing_key(self):
        self.assertIsNone(self.cache.get("nonexistent"))

    def test_ttl_expiration(self):
        self.cache.set("k1", "value", ttl=1)
        self.assertEqual(self.cache.get("k1"), "value")
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("k1"))

    def test_delete(self):
        self.cache.set("k1", "value")
        self.assertTrue(self.cache.delete("k1"))
        self.assertIsNone(self.cache.get("k1"))

    def test_delete_missing(self):
        self.assertFalse(self.cache.delete("nonexistent"))

    def test_invalidate_prefix(self):
        self.cache.set("rec:1576-C0001", "a")
        self.cache.set("rec:1576-C0002", "b")
        self.cache.set("match:1576-T0001", "c")
        removed = self.cache.invalidate_prefix("rec:")
        self.assertEqual(removed, 2)
        self.assertIsNone(self.cache.get("rec:1576-C0001"))
        self.assertEqual(self.cache.get("match:1576-T0001"), "c")

    def test_clear(self):
        self.cache.set("k1", "a")
        self.cache.set("k2", "b")
        self.cache.clear()
        self.assertIsNone(self.cache.get("k1"))
        self.assertIsNone(self.cache.get("k2"))

    def test_stats(self):
        self.cache.set("k1", "a")
        self.cache.set("k2", "b")
        stats = self.cache.stats()
        self.assertEqual(stats["total_keys"], 2)
        self.assertEqual(stats["active"], 2)

    def test_overwrite_key(self):
        self.cache.set("k1", "old")
        self.cache.set("k1", "new")
        self.assertEqual(self.cache.get("k1"), "new")


class TestCacheFactory(unittest.TestCase):
    def test_fallback_to_memory(self):
        cache = create_cache(redis_url=None)
        self.assertIsInstance(cache, TTLCache)

    def test_bad_redis_url_falls_back(self):
        cache = create_cache(redis_url="redis://localhost:99999/0")
        self.assertIsInstance(cache, TTLCache)


if __name__ == "__main__":
    unittest.main()
