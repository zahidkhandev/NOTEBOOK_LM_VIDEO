from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Text, func
from pgvector.sqlalchemy import Vector
from app.db.database import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), unique=True, nullable=False)

    script_embedding = Column(Vector(768), nullable=True)
    topic_embedding = Column(Vector(768), nullable=True)
    visual_style_embedding = Column(Vector(512), nullable=True)
    concept_embedding = Column(Vector(768), nullable=True)
    combined_embedding = Column(Vector(2048), nullable=True)

    embedding_model = Column(Text, default="text-embedding-004")
    model_version = Column(Text, default="1.0")
    
    quality_score = Column(Float, default=0.0)
    is_complete = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
