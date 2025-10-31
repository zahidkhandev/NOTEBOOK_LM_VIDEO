from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, func
from app.db.database import Base

class VideoRelationship(Base):
    __tablename__ = "video_relationships"

    id = Column(Integer, primary_key=True, index=True)
    
    video_id_1 = Column(Integer, ForeignKey("videos.id"), nullable=False, index=True)
    video_id_2 = Column(Integer, ForeignKey("videos.id"), nullable=False, index=True)
    
    relationship_type = Column(String(50), nullable=False, index=True)
    similarity_score = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)
    transition_count = Column(Integer, default=0)
    
    is_verified = Column(Integer, default=0)
    confidence = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ConceptRelationship(Base):
    __tablename__ = "concept_relationships"

    id = Column(Integer, primary_key=True, index=True)
    
    concept_id_1 = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    concept_id_2 = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    
    relationship_type = Column(String(50), nullable=False)
    strength = Column(Float, default=0.5)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
