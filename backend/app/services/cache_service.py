"""
Cache service - Redis compatible (in-memory fallback)
"""

import logging
import json
from typing import Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Cache service for storing and retrieving cached data."""
    
    def __init__(self):
        self._cache: dict = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            return self._cache.get(key)
        except Exception as e:
            logger.warning(f"⚠️ Cache get failed: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache."""
        try:
            ttl = ttl or settings.CACHE_TTL
            self._cache[key] = value
            logger.debug(f"✅ Cache set: {key}")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Cache set failed: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete from cache."""
        try:
            if key in self._cache:
                del self._cache[key]
            return True
        except Exception as e:
            logger.warning(f"⚠️ Cache delete failed: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> bool:
        """Clear cache keys matching pattern."""
        try:
            import fnmatch
            keys_to_delete = [k for k in self._cache.keys() if fnmatch.fnmatch(k, pattern)]
            for key in keys_to_delete:
                del self._cache[key]
            logger.debug(f"✅ Cleared {len(keys_to_delete)} cache entries")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Cache clear failed: {e}")
            return False
    
    async def health_check(self) -> bool:
        """Check cache health."""
        try:
            await self.set("health_check", "ok", ttl=1)
            return True
        except Exception as e:
            logger.error(f"❌ Cache health check failed: {e}")
            return False


_cache_service = None


def get_cache_service() -> CacheService:
    """Get or create cache service instance."""
    global _cache_service
    if _cache_service is None:
        _cache_service = CacheService()
    return _cache_service
