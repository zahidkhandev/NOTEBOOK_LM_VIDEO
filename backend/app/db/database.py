"""
Database configuration and session management.

Handles SQLAlchemy setup, pgvector extension initialization, and connection pooling.
"""

import logging
from typing import AsyncGenerator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

logger = logging.getLogger(__name__)

# ═════════════════════════════════════════════════════════════════════════════
# Database Setup
# ═════════════════════════════════════════════════════════════════════════════

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    pool_recycle=settings.DATABASE_POOL_RECYCLE,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.DATABASE_URL
    else {},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# ═════════════════════════════════════════════════════════════════════════════
# pgvector Extension
# ═════════════════════════════════════════════════════════════════════════════


def create_pgvector_extension() -> None:
    """
    Create pgvector extension in PostgreSQL.

    Required for vector similarity search operations.

    Raises:
        Exception: If extension creation fails
    """
    try:
        with engine.begin() as connection:
            connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            logger.info("✅ pgvector extension initialized")
    except Exception as e:
        logger.warning(f"⚠️  pgvector extension warning: {e}")


# Initialize pgvector on module import
if "postgresql" in settings.DATABASE_URL:
    try:
        create_pgvector_extension()
    except Exception as e:
        logger.error(f"❌ pgvector initialization failed: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# Session Management
# ═════════════════════════════════════════════════════════════════════════════


def get_db():
    """
    Get database session.

    Yields database session and ensures cleanup.

    Yields:
        Session: SQLAlchemy session

    Example:
        ```
        @app.get("/items")
        async def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ═════════════════════════════════════════════════════════════════════════════
# Health Checks
# ═════════════════════════════════════════════════════════════════════════════


async def check_database_health() -> bool:
    """
    Check database connection health.

    Attempts to execute a simple query to verify database connectivity.

    Returns:
        bool: True if database is accessible, False otherwise

    Example:
        ```
        health = await check_database_health()
        if not health:
            logger.error("Database unavailable")
        ```
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.debug("✅ Database health check passed")
        return True
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return False
