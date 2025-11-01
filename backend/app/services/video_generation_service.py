"""
Video generation service - Tortoise ORM with UTC timezone support
PRODUCTION GRADE - Complete service for video generation workflow
"""

import logging
from datetime import datetime, timezone

from app.models.models import Video
from app.core.constants import VideoStatus

logger = logging.getLogger(__name__)


class VideoGenerationService:
    """Handle video generation workflow and progress tracking."""
    
    async def update_video_progress(self, video_id: int, progress: int, status: str = None) -> Video:
        """
        Update video generation progress.
        
        Args:
            video_id: Video ID
            progress: Progress percentage (0-100)
            status: Optional status update
        
        Returns:
            Updated video object
        """
        try:
            video = await Video.get_or_none(id=video_id)
            if not video:
                logger.warning(f"⚠️ Video {video_id} not found for progress update")
                return None
            
            video.progress = max(0, min(100, progress))  # Clamp 0-100
            if status:
                video.status = status
                logger.debug(f"📊 Video {video_id} status → {status}")
            
            await video.save()
            logger.debug(f"✅ Video {video_id} progress: {video.progress}%")
            return video
        
        except Exception as e:
            logger.error(f"❌ Failed to update video progress: {e}", exc_info=True)
            raise
    
    async def mark_processing(self, video_id: int) -> Video:
        """
        Mark video as processing.
        
        Args:
            video_id: Video ID
        
        Returns:
            Updated video object
        """
        try:
            video = await Video.get_or_none(id=video_id)
            if not video:
                raise ValueError(f"Video {video_id} not found")
            
            video.status = VideoStatus.PROCESSING.value
            video.progress = 10
            await video.save()
            
            logger.info(f"✅ Video {video_id} marked as processing")
            return video
        except Exception as e:
            logger.error(f"❌ Failed to mark processing: {e}", exc_info=True)
            raise
    
    async def mark_completed(
        self,
        video_id: int,
        output_path: str,
        file_size: int,
        generation_time: float = None,
        quality_score: float = 0.9
    ) -> Video:
        """
        Mark video as completed.
        
        Args:
            video_id: Video ID
            output_path: Path to generated video file
            file_size: File size in bytes
            generation_time: Time taken to generate (seconds)
            quality_score: Quality score (0-1)
        
        Returns:
            Updated video object
        """
        try:
            video = await Video.get_or_none(id=video_id)
            if not video:
                raise ValueError(f"Video {video_id} not found")
            
            video.status = VideoStatus.COMPLETED.value
            video.progress = 100
            video.output_path = output_path
            video.file_size = file_size
            video.generation_time = generation_time
            video.quality_score = quality_score
            video.completed_at = datetime.now(timezone.utc)
            
            await video.save()
            
            logger.info(f"✅ Video {video_id} completed!")
            logger.info(f"   📁 Output: {output_path}")
            logger.info(f"   💾 Size: {file_size} bytes")
            logger.info(f"   ⏱️ Time: {generation_time:.1f}s")
            logger.info(f"   ⭐ Quality: {quality_score}/1.0")
            
            return video
        
        except Exception as e:
            logger.error(f"❌ Failed to mark completed: {e}", exc_info=True)
            raise
    
    async def mark_failed(self, video_id: int, error_message: str) -> Video:
        """
        Mark video as failed.
        
        Args:
            video_id: Video ID
            error_message: Error description
        
        Returns:
            Updated video object
        """
        try:
            video = await Video.get_or_none(id=video_id)
            if not video:
                logger.warning(f"⚠️ Video {video_id} not found for error marking")
                return None
            
            video.status = VideoStatus.FAILED.value
            video.error_message = error_message
            
            await video.save()
            
            logger.error(f"❌ Video {video_id} marked as FAILED")
            logger.error(f"   Error: {error_message}")
            
            return video
        
        except Exception as e:
            logger.error(f"❌ Failed to mark failed: {e}", exc_info=True)
            raise


def get_video_generation_service() -> VideoGenerationService:
    """Get video generation service instance (singleton-like)."""
    return VideoGenerationService()
