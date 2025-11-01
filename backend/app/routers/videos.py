"""
Video management and retrieval endpoints - Tortoise ORM
Handles video tracking, metadata, status, and deletion.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from app.models.models import Video
from app.services.cache_service import get_cache_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def list_videos(
    status_filter: Optional[str] = None,
    channel_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
):
    """List all generated videos with optional filters."""
    try:
        logger.debug(f"Fetching videos: status={status_filter}, channel={channel_id}")

        # ✅ Tortoise ORM
        query = Video.all()

        if status_filter:
            query = query.filter(status=status_filter)

        if channel_id:
            query = query.filter(channel_id=channel_id)

        total = await query.count()
        videos = await query.offset(skip).limit(limit)

        videos_list = [
            {
                "id": v.id,
                "title": v.title,
                "description": v.description,
                "duration": v.duration,
                "channel_id": v.channel_id,
                "status": v.status,
                "progress": v.progress,
                "quality_score": v.quality_score,
                "created_at": v.created_at.isoformat(),
                "completed_at": v.completed_at.isoformat() if v.completed_at else None,
            }
            for v in videos
        ]

        return {
            "videos": videos_list,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

    except Exception as e:
        logger.error(f"❌ Failed to list videos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve videos",
        )


@router.get("/{video_id}")
async def get_video(video_id: int):
    """Get video details and metadata."""
    try:
        logger.debug(f"Fetching video: {video_id}")

        # ✅ Tortoise ORM
        video = await Video.get_or_none(id=video_id)

        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found",
            )

        return {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "duration": video.duration,
            "channel_id": video.channel_id,
            "status": video.status,
            "progress": video.progress,
            "file_size": video.file_size,
            "quality_score": video.quality_score,
            "generation_time": video.generation_time,
            "error_message": video.error_message if video.status == "failed" else None,
            "created_at": video.created_at.isoformat(),
            "completed_at": video.completed_at.isoformat() if video.completed_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get video: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve video",
        )


@router.get("/{video_id}/download")
async def download_video(video_id: int):
    """Get video download URL."""
    try:
        logger.debug(f"Getting download info for video: {video_id}")

        # ✅ Tortoise ORM
        video = await Video.get_or_none(id=video_id)

        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found",
            )

        if video.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Video is {video.status}, not available for download",
            )

        return {
            "download_url": f"/videos/{video.id}",
            "filename": f"{video.title.replace(' ', '_')}.mp4",
            "file_size": video.file_size,
            "content_type": "video/mp4",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Download info failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get download info",
        )


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(video_id: int):
    """Delete a generated video."""
    try:
        logger.info(f"🗑️ Deleting video: {video_id}")

        # ✅ Tortoise ORM
        video = await Video.get_or_none(id=video_id)

        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found",
            )

        # ✅ Invalidate cache
        cache_service = get_cache_service()
        await cache_service.delete(f"video:{video_id}")

        # Delete from database
        await video.delete()

        logger.info(f"✅ Video deleted: {video_id}")
        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete video: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete video",
        )
