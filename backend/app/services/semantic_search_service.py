"""
Semantic search service for finding similar videos.

Uses embeddings and vector similarity to find related content.
"""

import logging
from typing import List, Optional

from app.services.embedding_service import get_embedding_service
from app.services.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class SemanticSearchService:
    """Service for semantic search operations."""

    def __init__(self):
        """Initialize semantic search service."""
        self.embedding_service = get_embedding_service()
        self.cache_service = get_cache_service()
        logger.info("✅ Semantic search service initialized")

    async def search_similar(
        self,
        query: str,
        videos: List[dict],
        top_k: int = 5,
    ) -> List[dict]:
        """
        Find similar videos to query.

        Args:
            query: Search query text
            videos: List of video documents with embeddings
            top_k: Number of results to return

        Returns:
            List of similar videos ranked by relevance

        Example:
            ```
            service = SemanticSearchService()
            results = await service.search_similar(
                "AI basics",
                videos,
                top_k=5
            )
            ```
        """
        try:
            # Check cache
            cache_key = f"search:{query}:{top_k}"
            cached = await self.cache_service.get(cache_key)
            if cached:
                logger.debug(f"✅ Search cache hit: {query}")
                return cached

            logger.info(f"🔍 Searching: {query}")

            # Generate query embedding
            query_embedding = await self.embedding_service.embed_text(query)
            if not query_embedding:
                logger.error("❌ Failed to embed query")
                return []

            # Calculate similarities
            results = []
            for video in videos:
                if not video.get("embedding"):
                    continue

                similarity = await self.embedding_service.similarity(
                    query_embedding,
                    video["embedding"],
                )

                if similarity >= 0.5:  # Threshold
                    results.append({
                        **video,
                        "similarity": similarity,
                    })

            # Sort by similarity
            results.sort(key=lambda x: x["similarity"], reverse=True)
            results = results[:top_k]

            # Cache results
            await self.cache_service.set(cache_key, results)

            logger.info(f"✅ Found {len(results)} similar videos")
            return results

        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []

    async def find_related_concepts(
        self,
        video_id: int,
        all_concepts: List[dict],
    ) -> List[dict]:
        """
        Find concepts related to video.

        Args:
            video_id: Video ID
            all_concepts: List of all concepts

        Returns:
            List of related concepts

        Example:
            ```
            service = SemanticSearchService()
            concepts = await service.find_related_concepts(1, all_concepts)
            ```
        """
        try:
            logger.debug(f"Finding concepts for video: {video_id}")

            # Implementation would fetch video embedding and find similar concepts
            related = []
            return related

        except Exception as e:
            logger.error(f"❌ Concept search failed: {e}")
            return []


# Singleton instance
_search_service: Optional[SemanticSearchService] = None


def get_semantic_search_service() -> SemanticSearchService:
    """
    Get or create semantic search service singleton.

    Returns:
        SemanticSearchService instance
    """
    global _search_service
    if _search_service is None:
        _search_service = SemanticSearchService()
    return _search_service
