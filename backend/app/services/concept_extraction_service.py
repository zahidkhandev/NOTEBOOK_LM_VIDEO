"""
Concept extraction service - Tortoise ORM
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class ConceptExtractionService:
    """Extract key concepts and topics from content."""
    
    async def extract_concepts(self, content: str) -> List[Dict]:
        """
        Extract key concepts from content using NLP.
        
        Args:
            content: Text content to analyze
        
        Returns:
            List of concepts with metadata
        """
        try:
            if not content or len(content.strip()) == 0:
                return []
            
            # Split by sentences for key points
            sentences = content.split('. ')
            concepts = []
            
            for sentence in sentences[:15]:
                sentence = sentence.strip()
                if len(sentence) > 10:  # Skip very short sentences
                    # Extract first 50 chars as concept name
                    concept_name = sentence[:100]
                    
                    concepts.append({
                        "name": concept_name,
                        "confidence": 0.85,
                        "category": "key_point",
                        "description": sentence
                    })
            
            logger.info(f"✅ Extracted {len(concepts)} concepts from content")
            return concepts
        
        except Exception as e:
            logger.error(f"❌ Concept extraction failed: {e}")
            return []
    
    async def extract_keywords(self, content: str, max_keywords: int = 10) -> List[str]:
        """Extract top keywords from content."""
        try:
            if not content:
                return []
            
            words = content.split()
            # Filter common words and get unique ones
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
            keywords = []
            
            for word in words:
                clean_word = word.lower().strip('.,!?;:')
                if clean_word not in common_words and len(clean_word) > 3:
                    if clean_word not in keywords:
                        keywords.append(clean_word)
                        if len(keywords) >= max_keywords:
                            break
            
            return keywords
        except Exception as e:
            logger.error(f"❌ Keyword extraction failed: {e}")
            return []


def get_concept_extraction_service() -> ConceptExtractionService:
    """Get concept extraction service instance."""
    return ConceptExtractionService()
