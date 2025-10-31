"""
FastAPI application factory and configuration.

Initializes the main application with middleware, routers, and health checks.
"""

import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import generation, sources, videos

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events.
    """
    # ─────────────────────────────────────────────────────────────────────────
    # Startup
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("🚀 Starting NotebookLM Video Generator API")

    # Create storage directories
    try:
        directories = [
            settings.GENERATED_DIR,
            settings.UPLOAD_DIR,
            settings.CACHE_DIR if hasattr(settings, "CACHE_DIR") else "storage/cache",
            settings.TEMP_DIR if hasattr(settings, "TEMP_DIR") else "storage/temp",
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            logger.debug(f"📁 Directory ready: {directory}")
    except Exception as e:
        logger.error(f"❌ Failed to create directories: {e}")
        raise

    # Initialize database
    try:
        from app.db.database import check_database_health

        db_health = await check_database_health()
        if db_health:
            logger.info("✅ Database connection established")
        else:
            logger.warning("⚠️  Database health check failed")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

    # Initialize cache
    try:
        from app.services.cache_service import get_cache_service

        cache_service = get_cache_service()
        await cache_service.health_check()
        logger.info("✅ Cache service initialized")
    except Exception as e:
        logger.warning(f"⚠️  Cache initialization: {e}")

    logger.info("✅ Application startup complete")
    yield

    # ─────────────────────────────────────────────────────────────────────────
    # Shutdown
    # ─────────────────────────────────────────────────────────────────────────
    logger.info("🛑 Shutting down NotebookLM Video Generator API")


# ═════════════════════════════════════════════════════════════════════════════
# Create FastAPI application
# ═════════════════════════════════════════════════════════════════════════════
app = FastAPI(
    title="NotebookLM Video Generator API",
    description="Generate NotebookLM-style educational videos from sources",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ═════════════════════════════════════════════════════════════════════════════
# Middleware
# ═════════════════════════════════════════════════════════════════════════════

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═════════════════════════════════════════════════════════════════════════════
# Static Files
# ═════════════════════════════════════════════════════════════════════════════

# Mount generated videos directory
if os.path.exists(settings.GENERATED_DIR):
    app.mount(
        "/videos",
        StaticFiles(directory=settings.GENERATED_DIR),
        name="videos",
    )
    logger.info(f"📁 Mounted video directory: {settings.GENERATED_DIR}")


# ═════════════════════════════════════════════════════════════════════════════
# Routers
# ═════════════════════════════════════════════════════════════════════════════

app.include_router(
    sources.router,
    prefix="/api/sources",
    tags=["sources"],
)

app.include_router(
    videos.router,
    prefix="/api/videos",
    tags=["videos"],
)

app.include_router(
    generation.router,
    prefix="/api/generate",
    tags=["generation"],
)


# ═════════════════════════════════════════════════════════════════════════════
# API Routes
# ═════════════════════════════════════════════════════════════════════════════


@app.get("/", tags=["health"])
async def root():
    """
    Root endpoint.

    Returns API information.

    Example:
        ```
        GET /

        Response:
        {
            "message": "NotebookLM Video Generator API",
            "version": "1.0.0",
            "docs": "/docs",
            "environment": "development"
        }
        ```
    """
    return {
        "message": "NotebookLM Video Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
async def health_check():
    """
    Quick health check endpoint.

    Returns:
        dict: API status and component health

    Example:
        ```
        GET /health

        Response:
        {
            "status": "healthy",
            "version": "1.0.0",
            "environment": "development",
            "components": {
                "api": "running",
                "database": "connected",
                "cache": "available"
            }
        }
        ```
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "running",
            "database": "connected",
            "cache": "available",
        },
    }


@app.get("/health/detailed", tags=["health"])
async def detailed_health_check():
    """
    Detailed health check endpoint.

    Returns comprehensive system status with all components.

    Returns:
        dict: Detailed health status

    Example:
        ```
        GET /health/detailed

        Response:
        {
            "status": "healthy",
            "timestamp": "2025-11-01T00:15:00Z",
            "version": "1.0.0",
            "environment": "development",
            "components": {
                "api": "running",
                "database": "connected",
                "cache": "available",
                "storage": "ready"
            },
            "uptime_seconds": 3600
        }
        ```
    """
    try:
        from app.db.database import check_database_health

        db_health = await check_database_health()
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_health = False

    # Check cache health
    try:
        from app.services.cache_service import get_cache_service

        cache_service = get_cache_service()
        await cache_service.health_check()
        cache_health = True
    except Exception as e:
        logger.warning(f"Cache health check failed: {e}")
        cache_health = False

    # Check storage
    storage_healthy = os.path.exists(settings.GENERATED_DIR) and os.path.exists(
        settings.UPLOAD_DIR
    )

    overall_status = (
        "healthy"
        if (db_health and cache_health and storage_healthy)
        else "degraded"
    )

    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "components": {
            "api": "running",
            "database": "connected" if db_health else "disconnected",
            "cache": "available" if cache_health else "unavailable",
            "storage": "ready" if storage_healthy else "missing",
        },
    }


# ═════════════════════════════════════════════════════════════════════════════
# Error Handlers
# ═════════════════════════════════════════════════════════════════════════════


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler.

    Logs errors and returns appropriate error responses.

    Args:
        request: Request object
        exc: Exception raised

    Returns:
        JSONResponse with error details
    """
    logger.error(f"❌ Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred",
            "timestamp": datetime.now().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
