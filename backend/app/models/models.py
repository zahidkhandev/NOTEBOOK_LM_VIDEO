"""
Tortoise ORM Models - AUTO MIGRATIONS
5-CHANNEL SUPPORT - ALL FIELDS COMPLETE
"""

from tortoise import fields, Model
from datetime import datetime
from typing import Optional


class Video(Model):
    """Video database model - LOCAL STORAGE ONLY."""
    
    id = fields.IntField(pk=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # Video Metadata
    # ─────────────────────────────────────────────────────────────────────
    title = fields.CharField(max_length=255, index=True)
    description = fields.TextField(null=True)
    duration = fields.IntField(default=60)
    
    # ─────────────────────────────────────────────────────────────────────
    # CHANNEL SUPPORT (5 channels)
    # ─────────────────────────────────────────────────────────────────────
    channel_id = fields.CharField(
        max_length=100,
        default="research_papers",
        index=True,
        description="research_papers|space_exploration|brainrot_grandfather|brainrot_stories|kids_brainrot"
    )
    category_name = fields.CharField(max_length=200, null=True)
    category_metadata = fields.JSONField(null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # CHARACTER SUPPORT
    # ─────────────────────────────────────────────────────────────────────
    characters_used = fields.JSONField(null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # CUSTOM PROMPT SUPPORT
    # ─────────────────────────────────────────────────────────────────────
    custom_prompt = fields.TextField(null=True)
    prompt_config = fields.CharField(max_length=50, null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # Status & Progress
    # ─────────────────────────────────────────────────────────────────────
    status = fields.CharField(max_length=50, default="pending", index=True)
    progress = fields.IntField(default=0)
    error_message = fields.TextField(null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # LOCAL FILE PATHS (NO CLOUD)
    # ─────────────────────────────────────────────────────────────────────
    output_path = fields.CharField(max_length=500, null=True)
    thumbnail_path = fields.CharField(max_length=500, null=True)
    script_path = fields.CharField(max_length=500, null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # Metrics
    # ─────────────────────────────────────────────────────────────────────
    generation_time = fields.FloatField(null=True)
    file_size = fields.IntField(null=True)
    quality_score = fields.FloatField(default=0.0)
    
    # ─────────────────────────────────────────────────────────────────────
    # Timestamps
    # ─────────────────────────────────────────────────────────────────────
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    completed_at = fields.DatetimeField(null=True)
    
    class Meta:
        table = "videos"
    
    def __str__(self) -> str:
        return f"<Video(id={self.id}, title='{self.title}', channel='{self.channel_id}', status='{self.status}')>"


class Source(Model):
    """Source document model - COMPLETE FIELDS."""
    
    id = fields.IntField(pk=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # File Information
    # ─────────────────────────────────────────────────────────────────────
    filename = fields.CharField(max_length=255)
    file_type = fields.CharField(max_length=20)  # pdf, docx, txt
    file_path = fields.CharField(max_length=500, null=True)
    file_size = fields.IntField(null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # Content
    # ─────────────────────────────────────────────────────────────────────
    content = fields.TextField()
    summary = fields.TextField(null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # Status & Processing
    # ─────────────────────────────────────────────────────────────────────
    status = fields.CharField(max_length=50, default="pending", index=True)
    error_message = fields.TextField(null=True)
    
    # ─────────────────────────────────────────────────────────────────────
    # Metadata
    # ─────────────────────────────────────────────────────────────────────
    language = fields.CharField(max_length=10, default="en")
    page_count = fields.IntField(null=True)
    word_count = fields.IntField(default=0)
    
    # ─────────────────────────────────────────────────────────────────────
    # Timestamps
    # ─────────────────────────────────────────────────────────────────────
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "sources"
    
    def __str__(self) -> str:
        return f"<Source(id={self.id}, filename='{self.filename}', status='{self.status}')>"


class Character(Model):
    """Character model for video generation."""
    
    id = fields.IntField(pk=True)
    channel_id = fields.CharField(max_length=100, index=True)
    character_name = fields.CharField(max_length=255)
    image_path = fields.CharField(max_length=500)
    metadata = fields.JSONField(null=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "characters"
    
    def __str__(self) -> str:
        return f"<Character(id={self.id}, name='{self.character_name}', channel='{self.channel_id}')>"


class GenerationJob(Model):
    """Background generation job tracking."""
    
    id = fields.IntField(pk=True)
    video_id = fields.IntField(index=True)
    job_id = fields.CharField(max_length=255, unique=True)
    status = fields.CharField(max_length=50, default="pending")
    progress = fields.IntField(default=0)
    error_message = fields.TextField(null=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "generation_jobs"
    
    def __str__(self) -> str:
        return f"<GenerationJob(id={self.id}, video_id={self.video_id}, status='{self.status}')>"
