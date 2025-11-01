"""
Semantic search service
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class SemanticSearchService:
    """Perform semantic search on content."""
    
    async def search(self, query: str, content: str, top_k: int = 5) -> List[Dict]:
        """
        Perform semantic search on content.
        
        Args:
            query: Search query
            content: Content to search in
            top_k: Number of results
        
        Returns:
            List of search results
        """
        try:
            sentences = content.split('. ')
            results = []
            
            for idx, sentence in enumerate(sentences[:top_k]):
                # Simple keyword matching as mock
                if any(word in sentence.lower() for word in query.lower().split()):
                    results.append({
                        "index": idx,
                        "text": sentence.strip(),
                        "score": 0.85
                    })
            
            logger.info(f"✅ Search found {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"❌ Semantic search failed: {e}")
            return []


def get_semantic_search_service() -> SemanticSearchService:
    """Get semantic search service instance."""
    return SemanticSearchService()
