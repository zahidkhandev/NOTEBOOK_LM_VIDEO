"""
FastAPI application with Tortoise ORM - AUTO MIGRATIONS
Async-first, no SQLAlchemy
CONSOLE LOGGING FORCED - ALL PRINT() VISIBLE
"""

import sys
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime

# ════════════════════════════════════════════════════════════════════════════
# FORCE CONSOLE OUTPUT - UNBUFFERED
# ════════════════════════════════════════════════════════════════════════════
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(line_buffering=True)
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(line_buffering=True)

# ════════════════════════════════════════════════════════════════════════════
# FORCE ALL LOGGING TO CONSOLE
# ════════════════════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    force=True,
)

# Force DEBUG for all loggers
for logger_name in ['', 'uvicorn', 'tortoise', 'asyncpg', 'app']:
    lg = logging.getLogger(logger_name)
    lg.setLevel(logging.DEBUG)
    lg.propagate = True

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.db.database import init_db, close_db, check_database_health
from app.routers import generation, sources, videos

logger = logging.getLogger(__name__)

print("\n" + "=" * 80)
print("🚀 STARTING NOTEBOOKLM VIDEO GENERATOR")
print("=" * 80 + "\n")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan - startup and shutdown with Tortoise ORM
    """
    
    # ─────────────────────────────────────────────────────────────────────
    # STARTUP
    # ─────────────────────────────────────────────────────────────────────
    print("🚀 Starting NotebookLM Video Generator API")
    logger.info("🚀 Starting NotebookLM Video Generator API")
    
    # ✅ Initialize Tortoise ORM and auto-create/update schemas
    try:
        print("📊 Initializing Tortoise ORM...")
        await init_db()
        print("✅ Database schemas synced!")
        logger.info("✅ Database schemas synced!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    # Check health
    try:
        print("🏥 Checking database health...")
        health = await check_database_health()
        if health:
            print("✅ Database connection established")
            logger.info("✅ Database connection established")
        else:
            print("⚠️ Database health check failed")
            logger.warning("⚠️ Database health check failed")
    except Exception as e:
        print(f"❌ Database health check error: {e}")
        logger.error(f"❌ Database health check error: {e}")
    
    # Create storage directories
    try:
        print("📁 Creating storage directories...")
        directories = [
            settings.GENERATED_DIR,
            settings.UPLOAD_DIR,
            settings.CACHE_DIR,
            settings.TEMP_DIR,
            settings.CHARACTER_DIR,
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ {directory}")
            logger.debug(f"📁 Directory ready: {directory}")
    except Exception as e:
        print(f"❌ Failed to create directories: {e}")
        logger.error(f"❌ Failed to create directories: {e}")
        raise
    
    print("\n✅ Application startup complete\n")
    logger.info("✅ Application startup complete")
    yield
    
    # ─────────────────────────────────────────────────────────────────────
    # SHUTDOWN
    # ─────────────────────────────────────────────────────────────────────
    print("\n🛑 Shutting down application")
    logger.info("🛑 Shutting down application")
    await close_db()
    print("✅ Application shutdown complete\n")
    logger.info("✅ Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="NotebookLM Video Generator API",
    description="Generate educational videos from sources - 5 CHANNELS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"✅ CORS configured for origins: {settings.CORS_ORIGINS[:2]}")
logger.info(f"✅ CORS configured")

# Mount generated videos directory
if os.path.exists(settings.GENERATED_DIR):
    app.mount(
        "/videos",
        StaticFiles(directory=settings.GENERATED_DIR),
        name="videos",
    )
    print(f"✅ Mounted video directory: {settings.GENERATED_DIR}")
    logger.info(f"📁 Mounted video directory: {settings.GENERATED_DIR}")


# Include routers
app.include_router(sources.router, prefix="/api/sources", tags=["sources"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(generation.router, prefix="/api/generate", tags=["generation"])

print(f"✅ Routers included: sources, videos, generation")
logger.info(f"✅ Routers included: sources, videos, generation")

# Health checks
@app.get("/", tags=["health"])
async def root():
    """Root endpoint - returns API information."""
    return {
        "message": "NotebookLM Video Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
async def health_check():
    """Quick health check endpoint."""
    db_health = await check_database_health()
    return {
        "status": "healthy" if db_health else "degraded",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "running",
            "database": "connected" if db_health else "disconnected",
        },
    }


@app.get("/health/detailed", tags=["health"])
async def detailed_health_check():
    """Detailed health check endpoint."""
    try:
        db_health = await check_database_health()
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_health = False

    # Check storage
    storage_healthy = os.path.exists(settings.GENERATED_DIR) and os.path.exists(
        settings.UPLOAD_DIR
    )

    overall_status = "healthy" if (db_health and storage_healthy) else "degraded"

    return {
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "components": {
            "api": "running",
            "database": "connected" if db_health else "disconnected",
            "storage": "ready" if storage_healthy else "missing",
        },
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler - logs errors and returns appropriate responses."""
    print(f"\n❌ EXCEPTION: {exc}")
    import traceback
    traceback.print_exc()
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
    print("\n📌 Running: uvicorn app.main:app --reload --log-level debug\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
