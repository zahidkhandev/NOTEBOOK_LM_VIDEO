import enum

from app.db.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class SourceType(enum.Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    URL = "url"
    YOUTUBE = "youtube"


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=True)

    title = Column(String, nullable=False)
    source_type = Column(SQLEnum(SourceType), nullable=False)
    file_path = Column(String, nullable=True)
    url = Column(String, nullable=True)

    # Extracted content
    content = Column(Text)
    word_count = Column(Integer, default=0)

    # Metadata
    file_size = Column(Integer, nullable=True)  # bytes
    page_count = Column(Integer, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    video = relationship("Video", backref="sources")
