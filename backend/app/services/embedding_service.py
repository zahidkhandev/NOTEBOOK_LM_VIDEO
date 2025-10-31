"""
Embedding service for generating text embeddings.

Uses Google's embedding API to create vector representations of text.
"""

import logging
from typing import List, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self):
        """Initialize embedding service."""
        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.client = genai
            logger.info("✅ Embedding service initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize embedding service: {e}")
            self.client = None

    async def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector or None if failed

        Example:
            ```
            service = EmbeddingService()
            embedding = await service.embed_text("Hello world")
            ```
        """
        try:
            if not text or len(text.strip()) == 0:
                logger.warning("❌ Empty text provided")
                return None

            if not self.client:
                logger.error("❌ Embedding client not initialized")
                return None

            result = self.client.embed_content(
                model=f"models/{settings.EMBEDDING_MODEL}",
                content=text,
            )

            embedding = result["embedding"]
            logger.debug(f"✅ Generated embedding: {len(embedding)} dimensions")
            return embedding

        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {e}")
            return None

    async def embed_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Example:
            ```
            service = EmbeddingService()
            embeddings = await service.embed_batch(["text1", "text2"])
            ```
        """
        logger.info(f"📊 Generating {len(texts)} embeddings")
        embeddings = []

        for text in texts:
            embedding = await self.embed_text(text)
            embeddings.append(embedding)

        return embeddings

    async def similarity(
        self,
        embedding1: List[float],
        embedding2: List[float],
    ) -> float:
        """
        Calculate cosine similarity between embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Similarity score (0-1)

        Example:
            ```
            service = EmbeddingService()
            similarity = await service.similarity(emb1, emb2)
            ```
        """
        try:
            import numpy as np

            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)

            similarity = np.dot(vec1, vec2) / (
                np.linalg.norm(vec1) * np.linalg.norm(vec2)
            )

            return float(similarity)
        except Exception as e:
            logger.error(f"❌ Similarity calculation failed: {e}")
            return 0.0


# Singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service() -> EmbeddingService:
    """
    Get or create embedding service singleton.

    Returns:
        EmbeddingService instance

    Example:
        ```
        service = get_embedding_service()
        embedding = await service.embed_text("text")
        ```
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
