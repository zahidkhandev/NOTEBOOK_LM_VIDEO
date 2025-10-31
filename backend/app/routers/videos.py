"""
Video management and retrieval endpoints.

Handles video tracking, metadata, status, and deletion.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.video import Video
from app.core.constants import VideoStatus
from app.services.cache_service import get_cache_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def list_videos(
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    List all generated videos.

    Args:
        status_filter: Filter by status (pending|processing|completed|failed)
        skip: Number of records to skip
        limit: Number of records to return
        db: Database session

    Returns:
        dict: List of videos with metadata

    Example:
        ```
        GET /api/videos/?status_filter=completed&skip=0&limit=10

        Response:
        {
            "videos": [
                {
                    "id": 1,
                    "title": "My Video",
                    "duration": 300,
                    "status": "completed",
                    "url": "/videos/video_1.mp4",
                    "created_at": "2025-10-31T23:00:00Z"
                }
            ],
            "total": 1
        }
        ```
    """
    try:
        logger.debug(f"Fetching videos list: status={status_filter}")

        query = db.query(Video)

        if status_filter:
            query = query.filter(Video.status == status_filter)

        total = query.count()
        videos = query.offset(skip).limit(limit).all()

        videos_list = [
            {
                "id": v.id,
                "title": v.title,
                "description": v.description,
                "duration": v.duration,
                "status": v.status,
                "progress": v.progress,
                "url": f"/videos/{v.id}" if v.output_path else None,
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
async def get_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    """
    Get video details and metadata.

    Args:
        video_id: Video ID
        db: Database session

    Returns:
        dict: Video metadata and current status

    Raises:
        HTTPException: If video not found

    Example:
        ```
        GET /api/videos/1

        Response:
        {
            "id": 1,
            "title": "My Video",
            "description": "Video description",
            "duration": 300,
            "status": "completed",
            "progress": 100,
            "visual_style": "whiteboard",
            "url": "/videos/1",
            "file_size": 50000000,
            "quality_score": 0.92,
            "generation_time": 125.5,
            "created_at": "2025-10-31T23:00:00Z",
            "completed_at": "2025-10-31T23:02:05Z"
        }
        ```
    """
    try:
        logger.debug(f"Fetching video: {video_id}")

        video = db.query(Video).filter(Video.id == video_id).first()

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
            "visual_style": video.visual_style,
            "status": video.status,
            "progress": video.progress,
            "url": f"/videos/{video.id}" if video.output_path else None,
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
async def download_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    """
    Get video download URL.

    Args:
        video_id: Video ID
        db: Database session

    Returns:
        dict: Download URL and metadata

    Example:
        ```
        GET /api/videos/1/download

        Response:
        {
            "download_url": "/videos/video_1.mp4",
            "filename": "My_Video.mp4",
            "file_size": 50000000,
            "content_type": "video/mp4"
        }
        ```
    """
    try:
        logger.debug(f"Getting download info for video: {video_id}")

        video = db.query(Video).filter(Video.id == video_id).first()

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
async def delete_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a generated video.

    Args:
        video_id: Video ID
        db: Database session

    Returns:
        None

    Raises:
        HTTPException: If deletion fails

    Example:
        ```
        DELETE /api/videos/1

        Response: 204 No Content
        ```
    """
    try:
        logger.info(f"🗑️  Deleting video: {video_id}")

        video = db.query(Video).filter(Video.id == video_id).first()

        if not video:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found",
            )

        # Invalidate cache
        cache_service = get_cache_service()
        await cache_service.delete(f"video:{video_id}")

        # Delete from database
        db.delete(video)
        db.commit()

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
