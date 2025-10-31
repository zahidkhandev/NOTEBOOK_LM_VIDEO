"""
Video generation service for creating educational videos.

Orchestrates the complete video generation workflow.
"""

import logging
from typing import Optional, List
from datetime import datetime

from app.config import settings
from app.services.embedding_service import get_embedding_service
from app.services.concept_extraction_service import get_concept_extraction_service
from app.services.knowledge_graph_service import get_knowledge_graph_service

logger = logging.getLogger(__name__)


class VideoGenerationService:
    """Service for orchestrating video generation."""

    def __init__(self):
        """Initialize video generation service."""
        self.embedding_service = get_embedding_service()
        self.concept_service = get_concept_extraction_service()
        self.graph_service = get_knowledge_graph_service()
        logger.info("✅ Video generation service initialized")

    async def generate_video(
        self,
        title: str,
        sources: List[dict],
        duration: int = 300,
        style: str = "classic",
    ) -> dict:
        """
        Generate video from sources.

        Args:
            title: Video title
            sources: List of source documents
            duration: Video duration in seconds
            style: Visual style

        Returns:
            Video generation job details

        Example:
            ```
            service = VideoGenerationService()
            job = await service.generate_video(
                title="AI Basics",
                sources=[...],
                duration=300,
                style="whiteboard"
            )
            ```
        """
        try:
            logger.info(f"🎬 Starting video generation: {title}")

            # Step 1: Extract content from sources
            combined_content = await self._combine_sources(sources)
            if not combined_content:
                raise ValueError("No content extracted from sources")

            # Step 2: Extract concepts
            concepts = await self.concept_service.extract_concepts(combined_content)
            if not concepts:
                logger.warning("⚠️  No concepts extracted")
                concepts = []

            # Step 3: Build knowledge graph
            graph = await self.graph_service.build_concept_graph(concepts)

            # Step 4: Generate structure
            structure = await self._generate_video_structure(
                combined_content,
                concepts,
                duration,
            )

            # Step 5: Create embeddings for semantic learning
            embeddings = await self._generate_embeddings(structure)

            logger.info(f"✅ Video generation job created: {title}")

            return {
                "job_id": f"job_{datetime.now().timestamp()}",
                "title": title,
                "status": "pending",
                "progress": 0,
                "concepts": concepts,
                "structure": structure,
                "embeddings": embeddings,
            }

        except Exception as e:
            logger.error(f"❌ Video generation failed: {e}")
            return {
                "error": str(e),
                "status": "failed",
            }

    async def _combine_sources(self, sources: List[dict]) -> str:
        """Combine content from multiple sources."""
        try:
            content_parts = []
            for source in sources:
                if source.get("content"):
                    content_parts.append(source["content"])

            combined = "\n\n".join(content_parts)
            logger.debug(f"✅ Combined {len(sources)} sources")
            return combined

        except Exception as e:
            logger.error(f"❌ Source combination failed: {e}")
            return ""

    async def _generate_video_structure(
        self,
        content: str,
        concepts: List[dict],
        duration: int,
    ) -> dict:
        """Generate video slide structure."""
        try:
            logger.debug("Generating video structure")

            # Calculate slides based on duration
            num_slides = max(3, duration // 60)

            structure = {
                "title": "Video Structure",
                "slides": [],
                "total_slides": num_slides,
                "estimated_duration": duration,
            }

            # Create slide structure
            for i in range(num_slides):
                slide = {
                    "slide_number": i + 1,
                    "title": f"Slide {i + 1}",
                    "concepts": [c for c in concepts[i::num_slides]][:3],
                    "duration": duration // num_slides,
                }
                structure["slides"].append(slide)

            logger.info(f"✅ Generated {num_slides} slides")
            return structure

        except Exception as e:
            logger.error(f"❌ Structure generation failed: {e}")
            return {}

    async def _generate_embeddings(self, structure: dict) -> List[List[float]]:
        """Generate embeddings for semantic learning."""
        try:
            logger.debug("Generating semantic embeddings")

            embeddings = []
            for slide in structure.get("slides", []):
                text = f"{slide['title']} {slide.get('description', '')}"
                embedding = await self.embedding_service.embed_text(text)
                if embedding:
                    embeddings.append(embedding)

            logger.info(f"✅ Generated {len(embeddings)} embeddings")
            return embeddings

        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {e}")
            return []


# Singleton instance
_generation_service: Optional[VideoGenerationService] = None


def get_video_generation_service() -> VideoGenerationService:
    """
    Get or create video generation service singleton.

    Returns:
        VideoGenerationService instance
    """
    global _generation_service
    if _generation_service is None:
        _generation_service = VideoGenerationService()
    return _generation_service
