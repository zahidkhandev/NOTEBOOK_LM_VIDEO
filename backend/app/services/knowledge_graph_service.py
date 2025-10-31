"""
Knowledge graph service for building concept relationships.

Creates connections between concepts and videos for semantic learning.
"""

import logging
from typing import List, Optional, Tuple

from app.services.embedding_service import get_embedding_service
from app.services.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class KnowledgeGraphService:
    """Service for managing knowledge graphs."""

    def __init__(self):
        """Initialize knowledge graph service."""
        self.embedding_service = get_embedding_service()
        self.cache_service = get_cache_service()
        logger.info("✅ Knowledge graph service initialized")

    async def build_concept_graph(self, concepts: List[dict]) -> dict:
        """
        Build knowledge graph from concepts.

        Args:
            concepts: List of concepts

        Returns:
            Knowledge graph structure with relationships

        Example:
            ```
            service = KnowledgeGraphService()
            graph = await service.build_concept_graph(concepts)
            ```
        """
        try:
            logger.info(f"🔗 Building concept graph for {len(concepts)} concepts")

            graph = {
                "nodes": concepts,
                "edges": [],
            }

            # Find relationships between concepts
            for i, concept1 in enumerate(concepts):
                for concept2 in concepts[i + 1 :]:
                    similarity = await self._calculate_concept_similarity(
                        concept1,
                        concept2,
                    )

                    if similarity > 0.6:  # Threshold
                        edge = {
                            "source": concept1["name"],
                            "target": concept2["name"],
                            "weight": similarity,
                            "type": "related",
                        }
                        graph["edges"].append(edge)

            logger.info(f"✅ Built graph with {len(graph['edges'])} relationships")
            return graph

        except Exception as e:
            logger.error(f"❌ Graph building failed: {e}")
            return {"nodes": [], "edges": []}

    async def _calculate_concept_similarity(
        self,
        concept1: dict,
        concept2: dict,
    ) -> float:
        """
        Calculate similarity between two concepts.

        Args:
            concept1: First concept
            concept2: Second concept

        Returns:
            Similarity score (0-1)
        """
        try:
            # Combine name and description for better similarity
            text1 = f"{concept1['name']} {concept1.get('description', '')}"
            text2 = f"{concept2['name']} {concept2.get('description', '')}"

            emb1 = await self.embedding_service.embed_text(text1)
            emb2 = await self.embedding_service.embed_text(text2)

            if not emb1 or not emb2:
                return 0.0

            similarity = await self.embedding_service.similarity(emb1, emb2)
            return similarity

        except Exception as e:
            logger.debug(f"⚠️  Similarity calculation failed: {e}")
            return 0.0

    async def find_learning_path(
        self,
        start_concept: str,
        end_concept: str,
        graph: dict,
    ) -> List[str]:
        """
        Find learning path between concepts.

        Args:
            start_concept: Starting concept
            end_concept: Target concept
            graph: Knowledge graph

        Returns:
            Path through related concepts

        Example:
            ```
            service = KnowledgeGraphService()
            path = await service.find_learning_path("Basics", "Advanced", graph)
            ```
        """
        try:
            logger.debug(f"Finding path: {start_concept} -> {end_concept}")

            # Simple BFS implementation
            from collections import deque

            queue = deque([(start_concept, [start_concept])])
            visited = {start_concept}

            while queue:
                current, path = queue.popleft()

                if current == end_concept:
                    logger.info(f"✅ Found path: {' -> '.join(path)}")
                    return path

                # Find neighbors
                for edge in graph.get("edges", []):
                    if edge["source"] == current:
                        neighbor = edge["target"]
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append((neighbor, path + [neighbor]))

            logger.warning(f"⚠️  No path found")
            return []

        except Exception as e:
            logger.error(f"❌ Learning path search failed: {e}")
            return []

    async def get_related_concepts(
        self,
        concept_name: str,
        graph: dict,
        depth: int = 2,
    ) -> List[str]:
        """
        Get related concepts from knowledge graph.

        Args:
            concept_name: Starting concept
            graph: Knowledge graph
            depth: Search depth

        Returns:
            List of related concepts

        Example:
            ```
            service = KnowledgeGraphService()
            related = await service.get_related_concepts("AI", graph)
            ```
        """
        try:
            logger.debug(f"Finding related concepts for: {concept_name}")

            related = set()
            to_explore = [(concept_name, 0)]

            while to_explore:
                current, curr_depth = to_explore.pop(0)

                if curr_depth > depth:
                    continue

                for edge in graph.get("edges", []):
                    if edge["source"] == current and edge["target"] not in related:
                        related.add(edge["target"])
                        if curr_depth < depth:
                            to_explore.append((edge["target"], curr_depth + 1))

            logger.info(f"✅ Found {len(related)} related concepts")
            return list(related)

        except Exception as e:
            logger.error(f"❌ Related concepts search failed: {e}")
            return []


# Singleton instance
_graph_service: Optional[KnowledgeGraphService] = None


def get_knowledge_graph_service() -> KnowledgeGraphService:
    """
    Get or create knowledge graph service singleton.

    Returns:
        KnowledgeGraphService instance
    """
    global _graph_service
    if _graph_service is None:
        _graph_service = KnowledgeGraphService()
    return _graph_service
