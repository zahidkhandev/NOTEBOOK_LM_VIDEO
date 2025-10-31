"""
Configuration management for NotebookLM Video Generator.

Handles environment variables, defaults, and settings validation.
Uses Pydantic for type safety and validation.
"""

import logging
from typing import List

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application configuration with environment variable support."""

    # ═══════════════════════════════════════════════════════════════════════════
    # API Keys (with secure defaults for development)
    # ═══════════════════════════════════════════════════════════════════════════
    GEMINI_API_KEY: str = "test-key-dev"
    """Google Gemini API key for content generation"""

    GOOGLE_CLOUD_PROJECT_ID: str = "test-project-dev"
    """Google Cloud Project ID for API services"""

    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    """Path to Google Cloud credentials JSON file"""

    # ═══════════════════════════════════════════════════════════════════════════
    # Application Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    APP_NAME: str = "NotebookLM Video Generator"
    """Application display name"""

    DEBUG: bool = True
    """Enable debug mode"""

    ENVIRONMENT: str = "development"
    """Application environment: development, staging, production"""

    # ═══════════════════════════════════════════════════════════════════════════
    # CORS Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    """Allowed origins for CORS requests"""

    # ═══════════════════════════════════════════════════════════════════════════
    # File Storage Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    UPLOAD_DIR: str = "storage/sources"
    """Directory for uploaded source files"""

    GENERATED_DIR: str = "storage/outputs"
    """Directory for generated video outputs"""

    CACHE_DIR: str = "storage/cache"
    """Directory for cache files"""

    TEMP_DIR: str = "storage/temp"
    """Directory for temporary files"""

    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024
    """Maximum upload file size in bytes (100 MB)"""

    # ═══════════════════════════════════════════════════════════════════════════
    # Database Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    DATABASE_URL: str = "postgresql://postgres:123@localhost:5434/notebook_lm_db"
    """PostgreSQL connection URL"""

    DATABASE_ECHO: bool = False
    """Enable SQL query logging"""

    DATABASE_POOL_SIZE: int = 20
    """Database connection pool size"""

    DATABASE_POOL_RECYCLE: int = 3600
    """Database connection recycle time (seconds)"""

    # ═══════════════════════════════════════════════════════════════════════════
    # Redis Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    REDIS_URL: str = "redis://:yourpassword@localhost:6379/0"
    """Redis connection URL"""

    REDIS_DB_NUMBER: int = 0
    """Redis database number"""

    CACHE_TTL: int = 3600
    """Cache TTL in seconds"""

    # ═══════════════════════════════════════════════════════════════════════════
    # Embeddings Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    EMBEDDING_MODEL: str = "text-embedding-004"
    """Model used for text embeddings"""

    EMBEDDING_DIMENSION: int = 768
    """Dimension of embedding vectors"""

    SIMILARITY_THRESHOLD: float = 0.7
    """Threshold for semantic similarity matching"""

    MAX_SEARCH_RESULTS: int = 5
    """Maximum search results to return"""

    SEARCH_CACHE_TTL: int = 3600
    """Cache TTL for search results (seconds)"""

    # ═══════════════════════════════════════════════════════════════════════════
    # Learning System Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    ENABLE_SEMANTIC_LEARNING: bool = True
    """Enable semantic learning from generated videos"""

    ENABLE_PATTERN_REUSE: bool = True
    """Enable pattern reuse for similar content"""

    MIN_CONFIDENCE_FOR_REUSE: float = 0.75
    """Minimum confidence score for pattern reuse"""

    AUTO_CONCEPT_EXTRACTION: bool = True
    """Automatically extract concepts from content"""

    # ═══════════════════════════════════════════════════════════════════════════
    # AWS/LocalStack Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    LOCALSTACK_ENDPOINT: str = "http://localhost:4566"
    """LocalStack endpoint for S3/DynamoDB"""

    AWS_REGION: str = "ap-south-1"
    """AWS region"""

    AWS_ACCESS_KEY_ID: str = "test"
    """AWS access key"""

    AWS_SECRET_ACCESS_KEY: str = "test"
    """AWS secret key"""

    S3_BUCKET_VIDEOS: str = "notebook-lm-videos-dev"
    """S3 bucket for video storage"""

    S3_BUCKET_EMBEDDINGS: str = "notebook-lm-embeddings-dev"
    """S3 bucket for embedding storage"""

    # ═══════════════════════════════════════════════════════════════════════════
    # Gemini Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    GEMINI_API_MODEL: str = "gemini-2.0-flash"
    """Gemini model version"""

    GEMINI_TEMPERATURE: float = 0.7
    """Temperature for Gemini generation (0-1)"""

    GEMINI_MAX_TOKENS: int = 2048
    """Maximum tokens for Gemini output"""

    # ═══════════════════════════════════════════════════════════════════════════
    # Video Generation Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    DEFAULT_DURATION: int = 300
    """Default video duration in seconds"""

    VIDEO_OUTPUT_DURATION_SHORTS: int = 120
    """Short-form video duration in seconds"""

    VIDEO_OUTPUT_DURATION_LONG: int = 300
    """Long-form video duration in seconds"""

    DEFAULT_STYLE: str = "whiteboard"
    """Default video style"""

    MAX_SLIDES: int = 50
    """Maximum slides per video"""

    MAX_PARALLEL_GENERATIONS: int = 2
    """Maximum parallel video generations"""

    VIDEO_FPS: int = 30
    """Video frames per second"""

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = True


# ═════════════════════════════════════════════════════════════════════════════
# Initialize settings
# ═════════════════════════════════════════════════════════════════════════════
try:
    settings = Settings()
    logger.info(f"✅ Configuration loaded: {settings.ENVIRONMENT}")
except Exception as e:
    logger.error(f"❌ Failed to load configuration: {e}")
    raise
