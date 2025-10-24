from typing import List

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
async def list_videos():
    """List all generated videos"""
    return {"videos": []}


@router.get("/{video_id}")
async def get_video(video_id: int):
    """Get video details"""
    return {"video_id": video_id}


@router.delete("/{video_id}")
async def delete_video(video_id: int):
    """Delete a video"""
    return {"message": "Video deleted"}
