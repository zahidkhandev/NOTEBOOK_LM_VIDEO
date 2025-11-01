"""
Application constants and configuration values.

Centralized definitions for magic numbers, strings, and enums.
"""

from enum import Enum


# ═════════════════════════════════════════════════════════════════════════════
# File Types
# ═════════════════════════════════════════════════════════════════════════════


class FileType(str, Enum):
    """Supported file types."""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    URL = "url"
    YOUTUBE = "youtube"


SUPPORTED_EXTENSIONS = {
    "pdf": ["application/pdf"],
    "docx": [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ],
    "txt": ["text/plain"],
}


# ═════════════════════════════════════════════════════════════════════════════
# Video Status
# ═════════════════════════════════════════════════════════════════════════════


class VideoStatus(str, Enum):
    """Video generation status values."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ═════════════════════════════════════════════════════════════════════════════
# Source Status
# ═════════════════════════════════════════════════════════════════════════════


class SourceStatus(str, Enum):
    """Source document status values."""

    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


# ═════════════════════════════════════════════════════════════════════════════
# Video Styles
# ═════════════════════════════════════════════════════════════════════════════


class VideoStyle(str, Enum):
    """Available video styles."""

    CLASSIC = "classic"
    WHITEBOARD = "whiteboard"
    WATERCOLOR = "watercolor"
    ANIME = "anime"
    RETRO = "retro"
    HERITAGE = "heritage"
    PAPERCRAFT = "papercraft"


# ═════════════════════════════════════════════════════════════════════════════
# Content Complexity Levels
# ═════════════════════════════════════════════════════════════════════════════


class ComplexityLevel(str, Enum):
    """Content complexity levels."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


# ═════════════════════════════════════════════════════════════════════════════
# Concept Categories
# ═════════════════════════════════════════════════════════════════════════════


class ConceptCategory(str, Enum):
    """Concept classification categories."""

    TOPIC = "topic"
    TECHNOLOGY = "technology"
    PERSON = "person"
    THEORY = "theory"
    METHOD = "method"
    TOOL = "tool"
    FRAMEWORK = "framework"


# ═════════════════════════════════════════════════════════════════════════════
# Error Messages
# ═════════════════════════════════════════════════════════════════════════════


ERROR_MESSAGES = {
    "invalid_file_type": "Unsupported file type. Supported types: PDF, DOCX, TXT",
    "file_too_large": "File exceeds maximum size limit (100 MB)",
    "no_content": "No content could be extracted from the file",
    "generation_failed": "Video generation failed. Please try again",
    "invalid_duration": "Duration must be between 60 and 600 seconds",
    "no_sources": "At least one source document is required",
}


# ═════════════════════════════════════════════════════════════════════════════
# Cache Keys
# ═════════════════════════════════════════════════════════════════════════════


CACHE_KEYS = {
    "search": "search:{query}:{top_k}",
    "embedding": "embedding:{text_hash}",
    "concepts": "concepts:{video_id}",
    "relationships": "relationships:{concept_id}",
    "video_status": "video_status:{video_id}",
}


# ═════════════════════════════════════════════════════════════════════════════
# Quality Thresholds
# ═════════════════════════════════════════════════════════════════════════════


QUALITY_THRESHOLDS = {
    "minimum_accuracy": 0.75,
    "minimum_clarity": 0.75,
    "minimum_engagement": 0.65,
    "similarity_threshold": 0.7,
    "concept_confidence_minimum": 0.5,
}


# ═════════════════════════════════════════════════════════════════════════════
# Timing Constants
# ═════════════════════════════════════════════════════════════════════════════


TIMING = {
    "reading_speed_wpm": 150,  # Words per minute
    "min_slide_duration": 2,  # Seconds
    "max_slide_duration": 15,  # Seconds
    "animation_duration": 1.5,  # Seconds
    "pause_duration": 0.5,  # Seconds
}


# ═════════════════════════════════════════════════════════════════════════════
# Rate Limiting & Timeouts (GEMINI FREE TIER)
# ═════════════════════════════════════════════════════════════════════════════


class RateLimits:
    """Gemini free tier rate limits."""

    RPM_LIMIT: int = 15  # Requests per minute
    REQUEST_INTERVAL: float = 4.0  # Seconds (60/15 = 4)
    DAILY_TOKEN_LIMIT: int = 1_000_000  # 1M tokens/day
    DAILY_REQUEST_LIMIT: int = 1_500  # 1500 requests/day
    TPM_LIMIT: int = 250_000  # Tokens per minute


class Timeouts:
    """API and service timeouts (in seconds)."""

    GEMINI_REQUEST: int = 30  # Gemini API call timeout
    VIDEO_GENERATION_MAX: int = 3600  # 1 hour max for video
    API_REQUEST: int = 60  # General API requests
    UPLOAD: int = 300  # File upload timeout
    POLLING_INTERVAL: int = 2  # Status check interval
    POLLING_MAX_ATTEMPTS: int = 300  # 10 minutes max (300 * 2s)


# ═════════════════════════════════════════════════════════════════════════════
# API Response Messages
# ═════════════════════════════════════════════════════════════════════════════


SUCCESS_MESSAGES = {
    "upload_complete": "File uploaded successfully",
    "generation_started": "Video generation has started",
    "generation_cancelled": "Video generation has been cancelled",
    "deletion_complete": "Resource has been deleted",
}
