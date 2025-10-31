"""
Cache management utilities.

Provides helpers for cache key generation and management.
"""

import logging
import hashlib
from typing import Any, Optional

from app.core.constants import CACHE_KEYS

logger = logging.getLogger(__name__)


class CacheKeyBuilder:
    """Builder for generating cache keys."""

    @staticmethod
    def search_key(query: str, top_k: int) -> str:
        """
        Build cache key for search results.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            Cache key

        Example:
            ```
            key = CacheKeyBuilder.search_key("AI basics", 5)
            ```
        """
        return f"search:{query}:{top_k}"

    @staticmethod
    def embedding_key(text: str) -> str:
        """
        Build cache key for embedding.

        Args:
            text: Text to embed

        Returns:
            Cache key with text hash

        Example:
            ```
            key = CacheKeyBuilder.embedding_key("Hello world")
            ```
        """
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"embedding:{text_hash}"

    @staticmethod
    def video_key(video_id: int) -> str:
        """
        Build cache key for video data.

        Args:
            video_id: Video ID

        Returns:
            Cache key

        Example:
            ```
            key = CacheKeyBuilder.video_key(123)
            ```
        """
        return f"video:{video_id}"

    @staticmethod
    def concept_key(video_id: int) -> str:
        """
        Build cache key for video concepts.

        Args:
            video_id: Video ID

        Returns:
            Cache key

        Example:
            ```
            key = CacheKeyBuilder.concept_key(123)
            ```
        """
        return f"concepts:{video_id}"

    @staticmethod
    def relationship_key(concept_id: int) -> str:
        """
        Build cache key for concept relationships.

        Args:
            concept_id: Concept ID

        Returns:
            Cache key

        Example:
            ```
            key = CacheKeyBuilder.relationship_key(456)
            ```
        """
        return f"relationships:{concept_id}"


class CacheInvalidator:
    """Cache invalidation utilities."""

    @staticmethod
    async def invalidate_video(cache_service, video_id: int) -> None:
        """
        Invalidate all caches related to a video.

        Args:
            cache_service: Cache service instance
            video_id: Video ID

        Example:
            ```
            await CacheInvalidator.invalidate_video(cache, 123)
            ```
        """
        try:
            keys = [
                CacheKeyBuilder.video_key(video_id),
                CacheKeyBuilder.concept_key(video_id),
                f"search:*video:{video_id}*",
            ]

            for key in keys:
                if "*" in key:
                    await cache_service.clear_pattern(key)
                else:
                    await cache_service.delete(key)

            logger.info(f"✅ Invalidated caches for video: {video_id}")

        except Exception as e:
            logger.error(f"❌ Cache invalidation failed: {e}")

    @staticmethod
    async def invalidate_concept(cache_service, concept_id: int) -> None:
        """
        Invalidate all caches related to a concept.

        Args:
            cache_service: Cache service instance
            concept_id: Concept ID

        Example:
            ```
            await CacheInvalidator.invalidate_concept(cache, 456)
            ```
        """
        try:
            await cache_service.delete(
                CacheKeyBuilder.relationship_key(concept_id)
            )
            logger.info(f"✅ Invalidated caches for concept: {concept_id}")

        except Exception as e:
            logger.error(f"❌ Cache invalidation failed: {e}")
