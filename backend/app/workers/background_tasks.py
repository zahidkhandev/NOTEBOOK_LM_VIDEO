"""
Background task handlers.

Manages long-running tasks like video generation and processing.
"""

import logging
import asyncio
from typing import Optional, Callable, Any
from datetime import datetime

from app.services.video_generation_service import get_video_generation_service
from app.services.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class TaskQueue:
    """In-memory task queue for background jobs."""

    def __init__(self):
        """Initialize task queue."""
        self.tasks = {}
        logger.info("✅ Task queue initialized")

    async def add_task(
        self,
        task_id: str,
        task_func: Callable,
        *args,
        **kwargs,
    ) -> dict:
        """
        Add task to queue.

        Args:
            task_id: Unique task ID
            task_func: Async function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Task info
        """
        try:
            self.tasks[task_id] = {
                "id": task_id,
                "status": "queued",
                "progress": 0,
                "created_at": datetime.now().isoformat(),
                "result": None,
                "error": None,
            }

            # Execute task
            asyncio.create_task(
                self._execute_task(task_id, task_func, args, kwargs)
            )

            logger.info(f"✅ Task queued: {task_id}")
            return self.tasks[task_id]

        except Exception as e:
            logger.error(f"❌ Failed to queue task: {e}")
            return {"error": str(e)}

    async def _execute_task(
        self,
        task_id: str,
        task_func: Callable,
        args: tuple,
        kwargs: dict,
    ) -> None:
        """Execute task and update status."""
        try:
            self.tasks[task_id]["status"] = "running"
            logger.info(f"🔄 Running task: {task_id}")

            result = await task_func(*args, **kwargs)

            self.tasks[task_id]["status"] = "completed"
            self.tasks[task_id]["result"] = result
            logger.info(f"✅ Task completed: {task_id}")

        except Exception as e:
            self.tasks[task_id]["status"] = "failed"
            self.tasks[task_id]["error"] = str(e)
            logger.error(f"❌ Task failed: {task_id} - {e}")

    async def get_task_status(self, task_id: str) -> Optional[dict]:
        """
        Get task status.

        Args:
            task_id: Task ID

        Returns:
            Task info or None
        """
        return self.tasks.get(task_id)

    async def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task.

        Args:
            task_id: Task ID

        Returns:
            True if cancelled
        """
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task["status"] in ["queued", "running"]:
                    task["status"] = "cancelled"
                    logger.info(f"✅ Task cancelled: {task_id}")
                    return True

            return False

        except Exception as e:
            logger.error(f"❌ Cancellation failed: {e}")
            return False


class VideoGenerationTask:
    """Video generation background task handler."""

    def __init__(self):
        """Initialize video generation task handler."""
        self.gen_service = get_video_generation_service()
        self.cache_service = get_cache_service()
        logger.info("✅ Video generation task handler initialized")

    async def generate_video(
        self,
        video_id: str,
        title: str,
        sources: list,
        duration: int,
        style: str,
    ) -> dict:
        """
        Generate video in background.

        Args:
            video_id: Video ID
            title: Video title
            sources: Source documents
            duration: Video duration
            style: Visual style

        Returns:
            Generation result
        """
        try:
            logger.info(f"🎬 Starting video generation: {video_id}")

            # Call generation service
            result = await self.gen_service.generate_video(
                title=title,
                sources=sources,
                duration=duration,
                style=style,
            )

            # Cache result
            cache_key = f"video:{video_id}"
            await self.cache_service.set(cache_key, result)

            logger.info(f"✅ Video generation complete: {video_id}")
            return result

        except Exception as e:
            logger.error(f"❌ Video generation failed: {e}")
            return {"error": str(e), "video_id": video_id}


# Global task queue instance
_task_queue: Optional[TaskQueue] = None


def get_task_queue() -> TaskQueue:
    """
    Get or create global task queue.

    Returns:
        TaskQueue instance
    """
    global _task_queue
    if _task_queue is None:
        _task_queue = TaskQueue()
    return _task_queue
