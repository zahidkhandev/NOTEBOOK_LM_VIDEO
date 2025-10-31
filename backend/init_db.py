"""Initialize database tables."""

from app.db.database import Base, engine
from app.models.video import Video
from app.models.source import Source
from app.models.embedding import Embedding
from app.models.concept import Concept
from app.models.relationship import VideoRelationship, ConceptRelationship

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")
