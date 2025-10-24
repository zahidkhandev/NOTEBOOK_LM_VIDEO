import enum

from app.db.database import Base
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func


class VideoStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    GENERATING_SLIDES = "generating_slides"
    GENERATING_IMAGES = "generating_images"
    GENERATING_AUDIO = "generating_audio"
    RENDERING = "rendering"
    COMPLETED = "completed"
    FAILED = "failed"


class VisualStyle(enum.Enum):
    CLASSIC = "classic"
    WHITEBOARD = "whiteboard"
    WATERCOLOR = "watercolor"
    RETRO = "retro"
    HERITAGE = "heritage"
    PAPERCRAFT = "papercraft"
    ANIME = "anime"


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, default=300)  # seconds
    visual_style = Column(SQLEnum(VisualStyle), default=VisualStyle.CLASSIC)
    status = Column(SQLEnum(VideoStatus), default=VideoStatus.PENDING)

    # Configuration
    config = Column(JSON)  # Stores slide count, narration speed, etc.

    # Generated assets
    script_data = Column(JSON)  # Full slide structure
    audio_file = Column(String, nullable=True)
    video_file = Column(String, nullable=True)

    # Metadata
    source_count = Column(Integer, default=0)
    slide_count = Column(Integer, default=0)
    word_count = Column(Integer, default=0)
    generation_cost = Column(Float, default=0.0)

    # Progress tracking
    progress_percentage = Column(Integer, default=0)
    current_step = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
