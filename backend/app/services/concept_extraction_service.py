"""
Concept extraction service for identifying key topics.

Uses Gemini API to automatically extract concepts from content.
"""

import logging
import json
from typing import List, Optional

from app.config import settings

logger = logging.getLogger(__name__)


class ConceptExtractionService:
    """Service for extracting concepts from content."""

    def __init__(self):
        """Initialize concept extraction service."""
        try:
            import google.generativeai as genai

            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.client = genai
            logger.info("✅ Concept extraction service initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize extraction service: {e}")
            self.client = None

    async def extract_concepts(self, text: str) -> List[dict]:
        """
        Extract key concepts from text.

        Args:
            text: Text to extract concepts from

        Returns:
            List of extracted concepts with metadata

        Example:
            ```
            service = ConceptExtractionService()
            concepts = await service.extract_concepts("AI is transforming...")
            ```
        """
        try:
            if not text or len(text.strip()) == 0:
                logger.warning("⚠️  Empty text provided")
                return []

            if not self.client:
                logger.error("❌ Extraction client not initialized")
                return []

            prompt = f"""
            Extract key concepts from this text. Return a JSON array with objects containing:
            - name: concept name
            - description: brief description
            - category: topic, technology, person, etc
            - confidence: 0-1 score

            Text:
            {text}

            Return only valid JSON array.
            """

            response = self.client.generate_content(
                prompt,
                generation_config={
                    "temperature": settings.GEMINI_TEMPERATURE,
                    "max_output_tokens": settings.GEMINI_MAX_TOKENS,
                },
            )

            # Parse response
            try:
                concepts = json.loads(response.text)
                logger.info(f"✅ Extracted {len(concepts)} concepts")
                return concepts
            except json.JSONDecodeError:
                logger.warning("⚠️  Invalid JSON in response")
                return []

        except Exception as e:
            logger.error(f"❌ Concept extraction failed: {e}")
            return []

    async def extract_hierarchy(self, concepts: List[dict]) -> dict:
        """
        Build concept hierarchy/taxonomy.

        Args:
            concepts: List of concepts

        Returns:
            Hierarchical concept structure

        Example:
            ```
            service = ConceptExtractionService()
            hierarchy = await service.extract_hierarchy(concepts)
            ```
        """
        try:
            if not concepts:
                return {}

            logger.debug(f"Building hierarchy for {len(concepts)} concepts")

            hierarchy = {
                "root": "Knowledge",
                "children": [],
            }

            # Group by category
            by_category = {}
            for concept in concepts:
                category = concept.get("category", "other")
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(concept)

            hierarchy["children"] = [
                {
                    "name": category,
                    "children": items,
                }
                for category, items in by_category.items()
            ]

            logger.info("✅ Concept hierarchy built")
            return hierarchy

        except Exception as e:
            logger.error(f"❌ Hierarchy extraction failed: {e}")
            return {}

    async def rank_concepts(self, concepts: List[dict]) -> List[dict]:
        """
        Rank concepts by importance.

        Args:
            concepts: List of concepts

        Returns:
            Ranked list of concepts

        Example:
            ```
            service = ConceptExtractionService()
            ranked = await service.rank_concepts(concepts)
            ```
        """
        try:
            # Sort by confidence score
            ranked = sorted(
                concepts,
                key=lambda x: x.get("confidence", 0),
                reverse=True,
            )

            logger.info(f"✅ Ranked {len(ranked)} concepts")
            return ranked

        except Exception as e:
            logger.error(f"❌ Concept ranking failed: {e}")
            return concepts


# Singleton instance
_extraction_service: Optional[ConceptExtractionService] = None


def get_concept_extraction_service() -> ConceptExtractionService:
    """
    Get or create concept extraction service singleton.

    Returns:
        ConceptExtractionService instance
    """
    global _extraction_service
    if _extraction_service is None:
        _extraction_service = ConceptExtractionService()
    return _extraction_service
