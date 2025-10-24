import os

from app.config import settings
from app.routers import generation, sources, videos
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="NotebookLM Video Generator API",
    description="Generate NotebookLM-style educational videos from sources",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
os.makedirs("data/generated/videos", exist_ok=True)
app.mount("/videos", StaticFiles(directory="data/generated/videos"), name="videos")

# Include routers
app.include_router(sources.router, prefix="/api/sources", tags=["sources"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(generation.router, prefix="/api/generate", tags=["generation"])


@app.get("/")
async def root():
    return {
        "message": "NotebookLM Video Generator API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
