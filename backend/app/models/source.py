"""
Source document model for database storage.

Represents uploaded source documents used for video generation.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, func

from app.db.database import Base


class Source(Base):
    """
    Source document database model.

    Stores uploaded documents with metadata and processing status.
    """

    __tablename__ = "sources"

    # ─────────────────────────────────────────────────────────────────────────
    # Primary Key
    # ─────────────────────────────────────────────────────────────────────────
    id = Column(Integer, primary_key=True, index=True)
    """Source ID"""

    # ─────────────────────────────────────────────────────────────────────────
    # File Information
    # ─────────────────────────────────────────────────────────────────────────
    filename = Column(String(255), nullable=False)
    """Original filename"""

    file_type = Column(String(20), nullable=False)
    """File type (pdf, docx, txt, url, youtube)"""

    file_path = Column(String(500), nullable=True)
    """Path to stored file"""

    file_size = Column(Integer, nullable=True)
    """File size in bytes"""

    # ─────────────────────────────────────────────────────────────────────────
    # Content
    # ─────────────────────────────────────────────────────────────────────────
    content = Column(Text, nullable=True)
    """Extracted text content"""

    summary = Column(Text, nullable=True)
    """AI-generated summary"""

    # ─────────────────────────────────────────────────────────────────────────
    # Status & Processing
    # ─────────────────────────────────────────────────────────────────────────
    status = Column(String(50), default="pending", index=True)
    """Processing status: pending, processing, ready, failed"""

    error_message = Column(Text, nullable=True)
    """Error message if processing failed"""

    # ─────────────────────────────────────────────────────────────────────────
    # Metadata
    # ─────────────────────────────────────────────────────────────────────────
    language = Column(String(10), default="en")
    """Document language"""

    page_count = Column(Integer, nullable=True)
    """Number of pages (for PDFs)"""

    word_count = Column(Integer, nullable=True)
    """Total word count"""

    # ─────────────────────────────────────────────────────────────────────────
    # Timestamps
    # ─────────────────────────────────────────────────────────────────────────
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    """Upload timestamp"""

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=False,
    )
    """Last update timestamp"""

    def __repr__(self) -> str:
        """String representation."""
        return f"<Source(id={self.id}, filename='{self.filename}', status='{self.status}')>"
