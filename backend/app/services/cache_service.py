"""
Cache service for Redis-based caching.

Handles caching of embeddings, search results, and generated content.
"""

import json
import logging
from typing import Any, Optional

import redis

from app.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Redis caching service."""

    def __init__(self):
        """Initialize Redis connection."""
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.redis_client.ping()
            logger.info("✅ Redis connection established")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.redis_client = None

    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found

        Example:
            ```
            cache = CacheService()
            value = await cache.get("user:123")
            ```
        """
        try:
            if not self.redis_client:
                return None

            value = self.redis_client.get(key)
            if value:
                logger.debug(f"✅ Cache hit: {key}")
                return json.loads(value)

            logger.debug(f"⚠️  Cache miss: {key}")
            return None
        except Exception as e:
            logger.error(f"❌ Cache get failed: {e}")
            return None

    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (uses CACHE_TTL if not specified)

        Returns:
            True if successful, False otherwise

        Example:
            ```
            cache = CacheService()
            await cache.set("user:123", {"id": 123, "name": "John"}, ttl=3600)
            ```
        """
        try:
            if not self.redis_client:
                return False

            ttl = ttl or settings.CACHE_TTL
            serialized = json.dumps(value)
            self.redis_client.setex(key, ttl, serialized)
            logger.debug(f"✅ Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"❌ Cache set failed: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.

        Args:
            key: Cache key

        Returns:
            True if successful

        Example:
            ```
            cache = CacheService()
            await cache.delete("user:123")
            ```
        """
        try:
            if not self.redis_client:
                return False

            self.redis_client.delete(key)
            logger.debug(f"🗑️  Cache deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"❌ Cache delete failed: {e}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching pattern.

        Args:
            pattern: Key pattern (e.g., "user:*")

        Returns:
            Number of keys deleted

        Example:
            ```
            cache = CacheService()
            deleted = await cache.clear_pattern("user:*")
            ```
        """
        try:
            if not self.redis_client:
                return 0

            keys = self.redis_client.keys(pattern)
            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"🗑️  Cleared {deleted} cache keys")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"❌ Cache clear failed: {e}")
            return 0

    async def health_check(self) -> bool:
        """
        Check Redis connection health.

        Returns:
            True if Redis is accessible

        Example:
            ```
            cache = CacheService()
            is_healthy = await cache.health_check()
            ```
        """
        try:
            if not self.redis_client:
                return False

            self.redis_client.ping()
            logger.debug("✅ Redis health check passed")
            return True
        except Exception as e:
            logger.error(f"❌ Redis health check failed: {e}")
            return False


# Singleton instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """
    Get or create cache service singleton.

    Returns:
        CacheService instance

    Example:
        ```
        cache = get_cache_service()
        value = await cache.get("key")
        ```
    """
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
