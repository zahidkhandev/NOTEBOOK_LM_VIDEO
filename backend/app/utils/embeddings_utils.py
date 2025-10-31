"""
Embedding utility functions.

Provides helper functions for embedding operations and similarity calculations.
"""

import logging
import numpy as np
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Similarity score between -1 and 1 (typically 0-1)

    Example:
        ```
        similarity = cosine_similarity(, )[1]
        ```
    """
    try:
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        similarity = dot_product / (norm_v1 * norm_v2)
        return float(similarity)

    except Exception as e:
        logger.error(f"❌ Similarity calculation failed: {e}")
        return 0.0


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate Euclidean distance between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Euclidean distance

    Example:
        ```
        distance = euclidean_distance(, )
        ```
    """
    try:
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        distance = np.linalg.norm(v1 - v2)
        return float(distance)

    except Exception as e:
        logger.error(f"❌ Distance calculation failed: {e}")
        return float("inf")


def normalize_embedding(embedding: List[float]) -> List[float]:
    """
    Normalize embedding vector to unit length.

    Args:
        embedding: Embedding vector

    Returns:
        Normalized embedding

    Example:
        ```
        normalized = normalize_embedding()[1]
        ```
    """
    try:
        vec = np.array(embedding)
        norm = np.linalg.norm(vec)

        if norm == 0:
            return embedding

        normalized = (vec / norm).tolist()
        return normalized

    except Exception as e:
        logger.error(f"❌ Normalization failed: {e}")
        return embedding


def find_nearest_neighbors(
    query_embedding: List[float],
    embeddings: List[List[float]],
    k: int = 5,
) -> List[Tuple[int, float]]:
    """
    Find k nearest neighbors to query embedding.

    Args:
        query_embedding: Query embedding vector
        embeddings: List of candidate embeddings
        k: Number of neighbors to return

    Returns:
        List of (index, similarity) tuples sorted by similarity

    Example:
        ```
        neighbors = find_nearest_neighbors(
            query_emb,
            all_embeddings,
            k=5
        )
        ```
    """
    try:
        similarities = []

        for idx, emb in enumerate(embeddings):
            sim = cosine_similarity(query_embedding, emb)
            similarities.append((idx, sim))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)

        logger.debug(f"✅ Found {len(similarities)} neighbors")
        return similarities[:k]

    except Exception as e:
        logger.error(f"❌ Neighbor search failed: {e}")
        return []


def batch_similarity(
    query_embeddings: List[List[float]],
    candidate_embeddings: List[List[float]],
) -> np.ndarray:
    """
    Calculate similarity matrix between query and candidate embeddings.

    Args:
        query_embeddings: List of query embeddings
        candidate_embeddings: List of candidate embeddings

    Returns:
        Similarity matrix (shape: queries x candidates)

    Example:
        ```
        similarity_matrix = batch_similarity(
            query_embs,
            candidate_embs
        )
        ```
    """
    try:
        queries = np.array(query_embeddings)
        candidates = np.array(candidate_embeddings)

        # Normalize for cosine similarity
        queries_norm = queries / np.linalg.norm(queries, axis=1, keepdims=True)
        candidates_norm = candidates / np.linalg.norm(
            candidates, axis=1, keepdims=True
        )

        # Compute similarity matrix
        similarity_matrix = np.dot(queries_norm, candidates_norm.T)

        logger.debug(
            f"✅ Computed similarity matrix: {similarity_matrix.shape}"
        )
        return similarity_matrix

    except Exception as e:
        logger.error(f"❌ Batch similarity failed: {e}")
        return np.array([])


def embedding_hash(embedding: List[float]) -> str:
    """
    Create hash of embedding for caching.

    Args:
        embedding: Embedding vector

    Returns:
        Hash string

    Example:
        ```
        hash_val = embedding_hash(embedding)
        ```
    """
    try:
        import hashlib

        # Convert to string and hash
        embedding_str = str(embedding)
        hash_obj = hashlib.sha256(embedding_str.encode())
        return hash_obj.hexdigest()

    except Exception as e:
        logger.error(f"❌ Hashing failed: {e}")
        return ""
