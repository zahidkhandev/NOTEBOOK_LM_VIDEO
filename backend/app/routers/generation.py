"""
Video generation endpoints.

Orchestrates video generation workflow from source to final output.
"""

import logging
import yaml
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.core.constants import VideoStatus
from app.db.database import get_db
from app.models.video import Video
from app.models.source import Source
from app.services.video_generation_service import get_video_generation_service
from app.services.concept_extraction_service import get_concept_extraction_service
from app.services.cache_service import get_cache_service
from app.workers.background_tasks import get_task_queue, VideoGenerationTask
from app.utils.validators import validate_duration, validate_text_length

logger = logging.getLogger(__name__)

router = APIRouter()


class VideoGenerationRequest(BaseModel):
    """Video generation request schema."""

    title: str = Field(..., min_length=1, max_length=200)
    """Video title"""

    description: str = Field(default="", max_length=1000)
    """Video description"""

    duration: int = Field(default=300, ge=60, le=600)
    """Video duration in seconds (1-10 minutes)"""

    visual_style: str = Field(default="classic")
    """Visual style (classic, whiteboard, watercolor, anime)"""

    source_ids: List[int] = Field(default=[])
    """List of source document IDs"""

    target_audience: str = Field(default="adult")
    """Target audience level (child, teen, adult)"""

    learning_objectives: Optional[List[str]] = Field(default=None)
    """Optional learning objectives"""

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "title": "Introduction to AI",
                "description": "A quick overview of artificial intelligence",
                "duration": 300,
                "visual_style": "whiteboard",
                "source_ids": [1, 2],
                "target_audience": "adult",
            }
        }


class VideoGenerationResponse(BaseModel):
    """Video generation response schema."""

    video_id: int
    """Generated video ID"""

    status: str
    """Generation status"""

    progress: int
    """Progress percentage"""

    job_id: Optional[str] = None
    """Background job ID"""

    message: str
    """Status message"""


def load_prompts():
    """Load prompt configurations from YAML files."""
    try:
        import os
        from pathlib import Path
        
        prompts_dir = Path("backend/prompts")
        prompts = {}
        
        for yaml_file in prompts_dir.glob("*.yaml"):
            if yaml_file.name == "config.yaml":
                continue
            
            with open(yaml_file, "r") as f:
                prompts.update(yaml.safe_load(f) or {})
        
        return prompts
    
    except Exception as e:
        logger.error(f"❌ Failed to load prompts: {e}")
        return {}


@router.post(
    "/start",
    response_model=VideoGenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_generation(
    request: VideoGenerationRequest,
    db: Session = Depends(get_db),
):
    """
    Start video generation process.

    Initiates asynchronous video generation based on sources and settings.

    Args:
        request: Video generation configuration
        db: Database session

    Returns:
        VideoGenerationResponse: Generation job details with tracking ID

    Raises:
        HTTPException: If generation fails to start

    Example:
        ```
        POST /api/generate/start
        Content-Type: application/json

        {
            "title": "My Video",
            "duration": 300,
            "visual_style": "whiteboard",
            "source_ids":,[1]
            "target_audience": "adult"
        }

        Response (202 Accepted):
        {
            "video_id": 1,
            "status": "pending",
            "progress": 0,
            "job_id": "job_1730393045.123",
            "message": "Video generation queued"
        }
        ```
    """
    try:
        # Validate inputs
        is_valid, error = validate_duration(request.duration)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error,
            )

        if not request.source_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one source document is required",
            )

        logger.info(f"🎬 Starting video generation: {request.title}")

        # Fetch sources
        sources = db.query(Source).filter(Source.id.in_(request.source_ids)).all()

        if len(sources) != len(request.source_ids):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Some source documents not found",
            )

        # Create video record
        video = Video(
            title=request.title,
            description=request.description,
            duration=request.duration,
            visual_style=request.visual_style,
            status=VideoStatus.PENDING.value,
            progress=0,
        )

        db.add(video)
        db.commit()
        db.refresh(video)

        logger.info(f"✅ Video job created: {video.id}")

        # Queue background task
        task_queue = get_task_queue()
        gen_task = VideoGenerationTask()

        sources_data = [
            {
                "id": s.id,
                "filename": s.filename,
                "content": s.content,
                "word_count": s.word_count,
            }
            for s in sources
        ]

        job = await task_queue.add_task(
            f"video_{video.id}",
            gen_task.generate_video,
            video_id=video.id,
            title=request.title,
            sources=sources_data,
            duration=request.duration,
            style=request.visual_style,
        )

        return VideoGenerationResponse(
            video_id=video.id,
            status="pending",
            progress=0,
            job_id=job.get("id"),
            message="Video generation queued",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to start generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start video generation",
        )


@router.get("/status/{video_id}", response_model=VideoGenerationResponse)
async def get_generation_status(
    video_id: int,
    db: Session = Depends(get_db),
):
    """
    Get video generation status.

    Returns current generation progress and status information.

    Args:
        video_id: Video ID
        db: Database session

    Returns:
        VideoGenerationResponse: Current generation status

    Raises:
        HTTPException: If video not found

    Example:
        ```
        GET /api/generate/status/1

        Response:
        {
            "video_id": 1,
            "status": "processing",
            "progress": 45,
            "message": "Generating slides..."
        }
        ```
    """
    try:
        logger.debug(f"Fetching generation status: {video_id}")

        video = db.query(Video).filter(Video.id == video_id).first()

        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found",
            )

        # Check cache for job status
        cache_service = get_cache_service()
        job_status = await cache_service.get(f"video_job:{video_id}")

        return VideoGenerationResponse(
            video_id=video.id,
            status=video.status,
            progress=video.progress,
            message=f"Video {video.status}: {video.progress}% complete",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get generation status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve generation status",
        )


@router.post("/cancel/{video_id}", status_code=status.HTTP_200_OK)
async def cancel_generation(
    video_id: int,
    db: Session = Depends(get_db),
):
    """
    Cancel ongoing video generation.

    Stops generation process for specified video.

    Args:
        video_id: Video ID to cancel
        db: Database session

    Returns:
        dict: Cancellation confirmation

    Raises:
        HTTPException: If cancellation fails

    Example:
        ```
        POST /api/generate/cancel/1

        Response:
        {
            "status": "cancelled",
            "message": "Video generation cancelled",
            "video_id": 1
        }
        ```
    """
    try:
        logger.info(f"❌ Cancelling generation: {video_id}")

        video = db.query(Video).filter(Video.id == video_id).first()

        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found",
            )

        if video.status not in ["pending", "processing"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot cancel video with status: {video.status}",
            )

        # Cancel task
        task_queue = get_task_queue()
        await task_queue.cancel_task(f"video_{video_id}")

        # Update video status
        video.status = VideoStatus.CANCELLED.value
        db.commit()

        logger.info(f"✅ Generation cancelled: {video_id}")

        return {
            "status": "cancelled",
            "message": "Video generation cancelled",
            "video_id": video_id,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to cancel generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel generation",
        )


@router.post("/analyze/{source_id}", status_code=status.HTTP_200_OK)
async def analyze_content(
    source_id: int,
    db: Session = Depends(get_db),
):
    """
    Analyze content and extract concepts for video generation.

    Pre-processes source content for generation.

    Args:
        source_id: Source ID
        db: Database session

    Returns:
        dict: Analysis results with concepts and structure

    Example:
        ```
        POST /api/generate/analyze/1

        Response:
        {
            "source_id": 1,
            "concepts": [
                {
                    "name": "Artificial Intelligence",
                    "confidence": 0.95,
                    "category": "topic"
                }
            ],
            "outline": {
                "slides": 7,
                "topics": ["AI Basics", "Machine Learning", ...]
            }
        }
        ```
    """
    try:
        logger.info(f"📊 Analyzing content: {source_id}")

        source = db.query(Source).filter(Source.id == source_id).first()

        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source not found",
            )

        if not source.content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Source has no content",
            )

        # Extract concepts
        concept_service = get_concept_extraction_service()
        concepts = await concept_service.extract_concepts(source.content)
        ranked_concepts = await concept_service.rank_concepts(concepts)

        return {
            "source_id": source_id,
            "concepts": ranked_concepts[:10],  # Top 10
            "total_concepts": len(ranked_concepts),
            "outline": {
                "estimated_slides": min(10, max(3, len(ranked_concepts))),
                "topics": [c["name"] for c in ranked_concepts[:5]],
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze content",
        )


@router.get("/templates")
async def get_templates():
    """
    Get available generation templates and configurations.

    Returns:
        dict: Available templates and styles

    Example:
        ```
        GET /api/generate/templates

        Response:
        {
            "styles": [
                {"name": "classic", "description": "Professional polished"},
                {"name": "whiteboard", "description": "Hand-drawn style"}
            ],
            "durations": ,
            "audiences": ["child", "teen", "adult"]
        }
        ```
    """
    try:
        prompts = load_prompts()
        config = prompts.get("generation", {})

        return {
            "styles": [
                {"name": s, "description": settings.ENVIRONMENT}
                for s in config.get("default_style", [])
            ],
            "durations": {
                "short": config.get("durations", {}).get("short", 120),
                "medium": config.get("durations", {}).get("medium", 300),
                "long": config.get("durations", {}).get("long", 600),
            },
            "audiences": ["child", "teen", "adult"],
            "complexity_levels": ["beginner", "intermediate", "advanced"],
        }

    except Exception as e:
        logger.error(f"❌ Failed to get templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve templates",
        )
