from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class VideoGenerationRequest(BaseModel):
    title: str
    duration: int = 300  # 5 minutes default
    visual_style: str = "classic"
    source_ids: List[int]


@router.post("/start")
async def start_generation(request: VideoGenerationRequest):
    """Start video generation process"""
    return {"message": "Video generation started", "video_id": 1, "status": "pending"}


@router.get("/status/{video_id}")
async def get_generation_status(video_id: int):
    """Get video generation status"""
    return {"video_id": video_id, "status": "processing", "progress": 45}


@router.post("/cancel/{video_id}")
async def cancel_generation(video_id: int):
    """Cancel video generation"""
    return {"message": "Generation cancelled"}
