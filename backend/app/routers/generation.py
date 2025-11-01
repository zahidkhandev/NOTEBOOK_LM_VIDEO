"""
Video generation endpoints - Tortoise ORM + 5 CHANNEL SUPPORT
Production-grade video generation orchestration with background task processing
and real-time Gemini API logging
"""

import logging
import yaml
import tempfile
from typing import List, Optional, Dict
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field

from app.config import settings
from app.core.constants import VideoStatus
from app.models.models import Video, Source
from app.services.video_generation_service import get_video_generation_service
from app.services.character_service import get_character_service
from app.services.concept_extraction_service import get_concept_extraction_service
from app.services.cache_service import get_cache_service
from app.utils.validators import validate_duration
from app.workers.background_tasks import run_video_generation_in_thread

logger = logging.getLogger(__name__)
router = APIRouter()


class VideoGenerationRequest(BaseModel):
    """Video generation request - ALL 5 CHANNELS."""
    
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    source_ids: List[int] = Field(default=[])
    channel_id: str = Field(
        default="research_papers",
        description="5 channels: research_papers|space_exploration|brainrot_grandfather|brainrot_stories|kids_brainrot"
    )
    duration: int = Field(default=60, ge=30, le=600)
    custom_prompt: Optional[str] = Field(default=None)
    target_audience: str = Field(default="adult")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "GPT-4 Breakthrough",
                "channel_id": "research_papers",
                "source_ids": [1],
                "duration": 60
            }
        }


class VideoGenerationResponse(BaseModel):
    """Response schema."""
    video_id: int
    channel_id: str
    status: str
    progress: int
    job_id: Optional[str] = None
    message: str


def load_channel_config(channel_id: str) -> Optional[Dict]:
    """Load channel configuration from YAML."""
    try:
        paths_to_try = [
            Path("prompts/channel_categories.yaml"),
            Path("backend/prompts/channel_categories.yaml"),
            Path(__file__).parent.parent.parent / "prompts" / "channel_categories.yaml",
        ]
        
        config_path = None
        for path in paths_to_try:
            if path.exists():
                config_path = path
                break
        
        if not config_path:
            logger.error(f"❌ channel_categories.yaml not found in any path")
            return None
        
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("channel_categories", {}).get(channel_id)
    except Exception as e:
        logger.error(f"❌ Failed to load channel config: {e}")
        return None


@router.post("/start", response_model=VideoGenerationResponse, status_code=status.HTTP_202_ACCEPTED)
async def start_generation(request: VideoGenerationRequest):
    """Start video generation for any of 5 channels with background task processing."""
    try:
        logger.info("=" * 80)
        logger.info(f"📌 NEW VIDEO GENERATION REQUEST")
        logger.info("=" * 80)
        
        # Validate channel
        channel_config = load_channel_config(request.channel_id)
        if not channel_config:
            logger.error(f"❌ Unknown channel: {request.channel_id}")
            raise HTTPException(
                status_code=400,
                detail=f"Unknown channel: {request.channel_id}"
            )
        
        logger.info(f"✅ Channel validated: {request.channel_id}")
        
        # Validate duration
        is_valid, error = validate_duration(request.duration)
        if not is_valid:
            logger.error(f"❌ Duration validation failed: {error}")
            raise HTTPException(status_code=400, detail=error)
        
        if not request.source_ids:
            logger.error("❌ No sources provided")
            raise HTTPException(status_code=400, detail="At least one source required")
        
        # ✅ Fetch sources (Tortoise ORM)
        sources = await Source.filter(id__in=request.source_ids)
        if len(sources) != len(request.source_ids):
            missing = set(request.source_ids) - {s.id for s in sources}
            logger.error(f"❌ Missing sources: {missing}")
            raise HTTPException(status_code=404, detail="Some sources not found")
        
        logger.info(f"✅ Sources found: {len(sources)}")
        
        # ✅ Create video record (Tortoise ORM - async)
        logger.info(f"📝 Creating video record...")
        video = await Video.create(
            title=request.title,
            description=request.description,
            duration=request.duration,
            channel_id=request.channel_id,
            category_name=channel_config.get("name"),
            category_metadata=channel_config.get("metadata"),
            custom_prompt=request.custom_prompt,
            prompt_config=request.channel_id,
            status=VideoStatus.PENDING.value,
            progress=0,
        )
        
        logger.info(f"✅ Video created: ID={video.id}, Status={video.status}")
        
        # ✅ USE VIDEO GENERATION SERVICE
        gen_service = get_video_generation_service()
        await gen_service.mark_processing(video.id)
        logger.info(f"✅ Video marked as processing")
        
        # ✅ USE CACHE SERVICE
        cache_service = get_cache_service()
        await cache_service.set(f"video:{video.id}", {
            "status": "processing",
            "progress": 10,
            "channel": request.channel_id,
            "queued_at": datetime.now(timezone.utc).isoformat()
        })
        logger.info(f"✅ Cache updated")
        
        # Prepare sources data
        sources_data = [
            {
                "id": s.id,
                "filename": s.filename,
                "content": s.content,
            }
            for s in sources
        ]
        
        # ✅ START BACKGROUND THREAD - THIS WILL RUN GEMINI CALLS
        logger.info(f"🔀 Starting background video generation thread...")
        
        run_video_generation_in_thread(
            video_id=video.id,
            title=request.title,
            sources=sources_data,
            channel_id=request.channel_id,
            duration=request.duration,
            custom_prompt=request.custom_prompt,
        )
        
        logger.info(f"✅ Background thread started!")
        logger.info("=" * 80)
        
        return VideoGenerationResponse(
            video_id=video.id,
            channel_id=request.channel_id,
            status="processing",
            progress=10,
            job_id=f"video_{video.id}",
            message=f"Video queued for {channel_config.get('name')} - Background generation started"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-character/{channel_id}")
async def upload_character_image(
    channel_id: str,
    file: UploadFile = File(...),
):
    """Upload character image for a channel - LOCAL STORAGE ONLY."""
    try:
        logger.info(f"📸 Uploading character image for channel: {channel_id}")
        
        char_service = get_character_service()
        
        # Save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        logger.info(f"✅ File saved to: {tmp_path}")
        
        # ✅ USE CHARACTER SERVICE (Tortoise ORM)
        if channel_id == "brainrot_grandfather":
            stored_path = await char_service.store_grandfather_character(tmp_path)
            logger.info(f"✅ Grandfather character stored: {stored_path}")
            return {
                "channel_id": channel_id,
                "character": "Grandfather",
                "image_path": stored_path,
                "message": "Grandfather image stored locally"
            }
        
        # For other channels, just store locally
        import os
        char_dir = settings.CHARACTER_DIR
        os.makedirs(char_dir, exist_ok=True)
        
        logger.info(f"✅ Character image stored for {channel_id}")
        return {
            "channel_id": channel_id,
            "image_path": tmp_path,
            "message": "Image uploaded (used next generation)"
        }
    
    except Exception as e:
        logger.error(f"❌ Character upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{video_id}", response_model=VideoGenerationResponse)
async def get_generation_status(video_id: int):
    """Get video generation status with real-time progress."""
    try:
        from app.workers.background_tasks import get_completed_video
        
        logger.debug(f"📊 Fetching status for video: {video_id}")
        
        # Check if background task completed it
        completed = get_completed_video(video_id)
        if completed:
            if completed["status"] == "completed":
                # Update DB now (in main thread - safe!)
                video = await Video.get_or_none(id=video_id)
                if video:
                    video.status = "completed"
                    video.progress = 100
                    video.output_path = completed["output_path"]
                    video.file_size = completed["file_size"]
                    video.generation_time = completed["generation_time"]
                    video.quality_score = completed["quality_score"]
                    video.completed_at = datetime.fromisoformat(completed["completed_at"])
                    await video.save()
                    logger.info(f"✅ Video {video_id} updated from background")
            else:
                # Mark failed
                video = await Video.get_or_none(id=video_id)
                if video:
                    video.status = "failed"
                    video.error_message = completed.get("error")
                    await video.save()
        
        # Get from DB
        video = await Video.get_or_none(id=video_id)
        if not video:
            logger.warning(f"⚠️ Video not found: {video_id}")
            raise HTTPException(status_code=404, detail="Video not found")
        
        logger.debug(f"✅ Video {video_id}: {video.status} ({video.progress}%)")
        
        return VideoGenerationResponse(
            video_id=video.id,
            channel_id=video.channel_id,
            status=video.status,
            progress=video.progress,
            message=f"Status: {video.status} ({video.progress}%)"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Status fetch failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cancel/{video_id}", status_code=status.HTTP_200_OK)
async def cancel_generation(video_id: int):
    """Cancel video generation."""
    try:
        logger.info(f"🛑 Cancelling video generation: {video_id}")
        
        # ✅ Tortoise ORM query
        video = await Video.get_or_none(id=video_id)
        if not video:
            logger.warning(f"⚠️ Video not found: {video_id}")
            raise HTTPException(status_code=404, detail="Video not found")
        
        if video.status not in ["pending", "processing"]:
            logger.error(f"❌ Cannot cancel video with status: {video.status}")
            raise HTTPException(status_code=400, detail=f"Cannot cancel: {video.status}")
        
        # ✅ USE VIDEO GENERATION SERVICE
        gen_service = get_video_generation_service()
        await gen_service.mark_failed(video_id, "Cancelled by user")
        
        # ✅ USE CACHE SERVICE
        cache_service = get_cache_service()
        await cache_service.delete(f"video:{video_id}")
        
        logger.info(f"✅ Video {video_id} cancelled")
        return {"status": "cancelled", "video_id": video_id}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Cancellation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/{source_id}", status_code=status.HTTP_200_OK)
async def analyze_content(source_id: int):
    """Analyze content and extract concepts."""
    try:
        logger.info(f"🔍 Analyzing source: {source_id}")
        
        # ✅ Tortoise ORM query
        source = await Source.get_or_none(id=source_id)
        if not source:
            logger.warning(f"⚠️ Source not found: {source_id}")
            raise HTTPException(status_code=404, detail="Source not found")
        
        if not source.content:
            logger.error(f"❌ Source has no content: {source_id}")
            raise HTTPException(status_code=400, detail="Source has no content")
        
        # ✅ USE CONCEPT EXTRACTION SERVICE
        concept_service = get_concept_extraction_service()
        concepts = await concept_service.extract_concepts(source.content)
        keywords = await concept_service.extract_keywords(source.content)
        
        # ✅ USE CACHE SERVICE
        cache_service = get_cache_service()
        await cache_service.set(f"analysis:{source_id}", {
            "concepts": concepts,
            "keywords": keywords
        })
        
        logger.info(f"✅ Analyzed source {source_id}: {len(concepts)} concepts, {len(keywords)} keywords")
        
        return {
            "source_id": source_id,
            "concepts": concepts[:10],
            "keywords": keywords,
            "total_concepts": len(concepts),
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_templates():
    """Get all 5 channels info."""
    try:
        logger.debug("📋 Fetching channel templates...")
        
        paths_to_try = [
            Path("prompts/channel_categories.yaml"),
            Path("backend/prompts/channel_categories.yaml"),
        ]
        
        for path in paths_to_try:
            if path.exists():
                with open(path) as f:
                    data = yaml.safe_load(f)
                
                channels = data.get("channel_categories", {})
                logger.info(f"✅ Loaded {len(channels)} channels")
                
                return {
                    "channels": [
                        {
                            "id": ch_id,
                            "name": ch.get("name"),
                            "description": ch.get("description"),
                            "default_duration": ch.get("default_duration"),
                            "video_style": ch.get("video_style"),
                            "tone": ch.get("tone"),
                            "audience": ch.get("metadata", {}).get("audience", [])
                        }
                        for ch_id, ch in channels.items()
                    ]
                }
        
        logger.error("❌ Channel config not found")
        raise HTTPException(status_code=500, detail="Channel config not found")
    
    except Exception as e:
        logger.error(f"❌ Templates fetch failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.post("/cleanup-pending", status_code=status.HTTP_200_OK)
async def cleanup_pending_tasks():
    """Delete all pending/processing videos."""
    try:
        logger.info("🧹 Cleaning up all pending tasks...")
        
        # Tortoise ORM filter syntax
        pending_videos = await Video.filter(status__in=["pending", "processing"])
        deleted_count = len(pending_videos)
        
        for video in pending_videos:
            await video.delete()
        
        logger.info(f"✅ Deleted {deleted_count} pending/processing videos")
        return {
            "status": "success",
            "deleted_count": deleted_count,
            "message": f"Cleaned up {deleted_count} pending tasks"
        }
    
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/force-complete/{video_id}", status_code=status.HTTP_200_OK)
async def force_complete_video(video_id: int):
    """Force mark video as completed (for testing)."""
    try:
        logger.info(f"🔨 Force completing video: {video_id}")
        
        video = await Video.get_or_none(id=video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        gen_service = get_video_generation_service()
        await gen_service.mark_completed(
            video_id=video_id,
            output_path=f"storage/outputs/video_{video_id}.mp4",
            file_size=50000000,
            generation_time=120.5,
            quality_score=0.92
        )
        
        logger.info(f"✅ Video {video_id} force completed")
        return {
            "status": "success",
            "video_id": video_id,
            "message": "Video force completed"
        }
    
    except Exception as e:
        logger.error(f"❌ Force complete failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
