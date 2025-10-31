"""
Video model for database storage.

Represents generated videos with metadata, embeddings, and relationships.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Video(Base):
    """
    Video database model.

    Stores video metadata, generation parameters, and performance metrics.
    """

    __tablename__ = "videos"

    # ─────────────────────────────────────────────────────────────────────────
    # Primary Key
    # ─────────────────────────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)
    """Video ID"""

    # ─────────────────────────────────────────────────────────────────────────
    # Video Metadata
    # ─────────────────────────────────────────────────────────────────────────
    title = Column(String(255), nullable=False, index=True)
    """Video title"""

    description = Column(Text, nullable=True)
    """Video description"""

    duration = Column(Integer, default=300)
    """Video duration in seconds"""

    visual_style = Column(String(50), default="classic")
    """Visual style (classic, whiteboard, watercolor, etc)"""

    # ─────────────────────────────────────────────────────────────────────────
    # Status & Progress
    # ─────────────────────────────────────────────────────────────────────────
    status = Column(String(50), default="pending", index=True)
    """Generation status: pending, processing, completed, failed"""

    progress = Column(Integer, default=0)
    """Progress percentage (0-100)"""

    error_message = Column(Text, nullable=True)
    """Error message if generation failed"""

    # ─────────────────────────────────────────────────────────────────────────
    # Output Files
    # ─────────────────────────────────────────────────────────────────────────
    output_path = Column(String(500), nullable=True)
    """Path to generated video file"""

    thumbnail_path = Column(String(500), nullable=True)
    """Path to video thumbnail"""

    # ─────────────────────────────────────────────────────────────────────────
    # Metrics
    # ─────────────────────────────────────────────────────────────────────────
    generation_time = Column(Float, nullable=True)
    """Time taken to generate video (seconds)"""

    file_size = Column(Integer, nullable=True)
    """Output file size in bytes"""

    quality_score = Column(Float, default=0.0)
    """Quality score (0-1)"""

    # ─────────────────────────────────────────────────────────────────────────
    # Timestamps
    # ─────────────────────────────────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    """Creation timestamp"""

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=False,
    )
    """Last update timestamp"""

    completed_at = Column(DateTime(timezone=True), nullable=True)
    """Completion timestamp"""

    def __repr__(self) -> str:
        """String representation."""
        return f"<Video(id={self.id}, title='{self.title}', status='{self.status}')>"
