from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, func, Table
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from app.db.database import Base

video_concepts = Table(
    'video_concepts',
    Base.metadata,
    Column('video_id', Integer, ForeignKey('videos.id'), primary_key=True),
    Column('concept_id', Integer, ForeignKey('concepts.id'), primary_key=True),
    Column('confidence_score', Float, default=0.8),
    Column('context', Text, nullable=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), default="topic")
    
    embedding = Column(Vector(768), nullable=True)
    
    video_count = Column(Integer, default=0)
    frequency = Column(Integer, default=0)
    confidence = Column(Float, default=1.0)
    
    parent_concept_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
