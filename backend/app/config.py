"""
Configuration management for NotebookLM Video Generator.
Handles environment variables, defaults, and settings validation.
5-CHANNEL SUPPORT + RATE LIMITING + TIMEOUTS
Reads .env from PROJECT ROOT
"""

import logging
from typing import List
from pydantic_settings import BaseSettings
import sys
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.core.constants import RateLimits, Timeouts

logger = logging.getLogger(__name__)

# ✅ Calculate path to root .env
# From: backend/app/config.py
# Go up: config.py (app) -> app (backend) -> backend (root)
ROOT_DIR = Path(__file__).parent.parent.parent
ENV_FILE_PATH = ROOT_DIR / ".env"

logger.info(f"📍 Looking for .env at: {ENV_FILE_PATH}")


class Settings(BaseSettings):
    """Application configuration with environment variable support."""

    # ═════════════════════════════════════════════════════════════════════════
    # API Keys
    # ═════════════════════════════════════════════════════════════════════════
    GEMINI_API_KEY: str = "test-key-dev"
    GOOGLE_CLOUD_PROJECT_ID: str = "test-project-dev"
    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    # ═════════════════════════════════════════════════════════════════════════
    # Application Configuration
    # ═════════════════════════════════════════════════════════════════════════
    APP_NAME: str = "NotebookLM Video Generator"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # ═════════════════════════════════════════════════════════════════════════
    # CORS Configuration
    # ═════════════════════════════════════════════════════════════════════════
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # ═════════════════════════════════════════════════════════════════════════
    # File Storage Configuration (LOCAL ONLY - NO CLOUD)
    # ═════════════════════════════════════════════════════════════════════════
    UPLOAD_DIR: str = "storage/sources"
    GENERATED_DIR: str = "storage/outputs"
    CACHE_DIR: str = "storage/cache"
    TEMP_DIR: str = "storage/temp"
    CHARACTER_DIR: str = "storage/characters"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024

    # ═════════════════════════════════════════════════════════════════════════
    # Database Configuration (Tortoise ORM)
    # ═════════════════════════════════════════════════════════════════════════
    DB_HOST: str = "localhost"
    DB_PORT: int = 5434
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123"
    DB_NAME: str = "notebook_lm_db"

    # ═════════════════════════════════════════════════════════════════════════
    # Redis Configuration
    # ═════════════════════════════════════════════════════════════════════════
    REDIS_URL: str = "redis://:yourpassword@localhost:6379/0"
    REDIS_DB_NUMBER: int = 0
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_SOCKET_CONNECT_TIMEOUT: int = 5
    CACHE_TTL: int = 3600

    # ═════════════════════════════════════════════════════════════════════════
    # Embeddings Configuration
    # ═════════════════════════════════════════════════════════════════════════
    EMBEDDING_MODEL: str = "text-embedding-004"
    EMBEDDING_DIMENSION: int = 768
    SIMILARITY_THRESHOLD: float = 0.7
    MAX_SEARCH_RESULTS: int = 5
    SEARCH_CACHE_TTL: int = 3600

    # ═════════════════════════════════════════════════════════════════════════
    # Learning System Configuration
    # ═════════════════════════════════════════════════════════════════════════
    ENABLE_SEMANTIC_LEARNING: bool = True
    ENABLE_PATTERN_REUSE: bool = True
    MIN_CONFIDENCE_FOR_REUSE: float = 0.75
    AUTO_CONCEPT_EXTRACTION: bool = True

    # ═════════════════════════════════════════════════════════════════════════
    # 5-CHANNEL CONFIGURATION
    # ═════════════════════════════════════════════════════════════════════════
    ACTIVE_CHANNELS: List[str] = [
        "research_papers",
        "space_exploration",
        "brainrot_grandfather",
        "brainrot_stories",
        "kids_brainrot",
    ]
    CHANNEL_PROMPTS_DIR: str = "backend/prompts"

    # ═════════════════════════════════════════════════════════════════════════
    # Gemini AI Configuration + RATE LIMITING
    # ═════════════════════════════════════════════════════════════════════════
    GEMINI_API_MODEL: str = "gemini-2.0-flash"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 2048
    GEMINI_RPM_LIMIT: int = RateLimits.RPM_LIMIT
    GEMINI_REQUEST_INTERVAL: float = RateLimits.REQUEST_INTERVAL
    GEMINI_DAILY_TOKEN_LIMIT: int = RateLimits.DAILY_TOKEN_LIMIT
    GEMINI_DAILY_REQUEST_LIMIT: int = RateLimits.DAILY_REQUEST_LIMIT
    GEMINI_TPM_LIMIT: int = RateLimits.TPM_LIMIT

    # ═════════════════════════════════════════════════════════════════════════
    # TIMEOUTS - Strict enforcement
    # ═════════════════════════════════════════════════════════════════════════
    API_REQUEST_TIMEOUT: int = Timeouts.GEMINI_REQUEST
    API_POLL_TIMEOUT: int = Timeouts.VIDEO_GENERATION_MAX
    POLLING_INTERVAL: int = Timeouts.POLLING_INTERVAL
    POLLING_MAX_ATTEMPTS: int = Timeouts.POLLING_MAX_ATTEMPTS
    UPLOAD_TIMEOUT: int = Timeouts.UPLOAD

    # ═════════════════════════════════════════════════════════════════════════
    # Video Generation Configuration
    # ═════════════════════════════════════════════════════════════════════════
    DEFAULT_DURATION: int = 60
    MIN_VIDEO_DURATION: int = 30
    MAX_VIDEO_DURATION: int = 600
    VIDEO_OUTPUT_DURATION_SHORTS: int = 45
    VIDEO_OUTPUT_DURATION_LONG: int = 300
    DEFAULT_STYLE: str = "whiteboard"
    MAX_SLIDES: int = 50
    MAX_PARALLEL_GENERATIONS: int = 2
    VIDEO_FPS: int = 30

    # ═════════════════════════════════════════════════════════════════════════
    # AWS/LocalStack Configuration (DISABLED FOR LOCAL STORAGE)
    # ═════════════════════════════════════════════════════════════════════════
    USE_LOCAL_STORAGE: bool = True
    LOCALSTACK_ENDPOINT: str = "http://localhost:4566"
    AWS_REGION: str = "ap-south-1"
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"
    S3_BUCKET_VIDEOS: str = "notebook-lm-videos-dev"
    S3_BUCKET_EMBEDDINGS: str = "notebook-lm-embeddings-dev"


    class Config:
        # ✅ POINT TO ROOT .env
        env_file = str(ENV_FILE_PATH)
        env_file_encoding = "utf-8"
        case_sensitive = True


try:
    settings = Settings()
    
    logger.info("=" * 80)
    logger.info("✅ Configuration loaded successfully!")
    logger.info("=" * 80)
    logger.info(f"🔑 GEMINI_API_KEY: {settings.GEMINI_API_KEY[:20]}...")
    logger.info(f"📌 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔐 Gemini Rate Limits: {settings.GEMINI_RPM_LIMIT} RPM")
    logger.info(
        f"⏱️  API Timeouts: {settings.API_REQUEST_TIMEOUT}s (requests), "
        f"{settings.API_POLL_TIMEOUT}s (generation)"
    )
    logger.info(
        f"📁 Storage: {settings.GENERATED_DIR} + {settings.CHARACTER_DIR} (LOCAL ONLY)"
    )
    logger.info(f"📊 Channels: {', '.join(settings.ACTIVE_CHANNELS)}")
    logger.info("=" * 80)
    
except Exception as e:
    logger.error(f"❌ Failed to load configuration: {e}")
    raise
