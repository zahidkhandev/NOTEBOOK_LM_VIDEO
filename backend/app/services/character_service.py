"""
Character management service - Tortoise ORM
"""

import logging
import os
from app.models.models import Character
from app.config import settings

logger = logging.getLogger(__name__)


class CharacterService:
    """Manage character images and metadata."""
    
    async def store_grandfather_character(self, file_path: str) -> str:
        """
        Store grandfather character image.
        
        Args:
            file_path: Path to character image
        
        Returns:
            Stored file path
        """
        try:
            char_dir = settings.CHARACTER_DIR
            os.makedirs(char_dir, exist_ok=True)
            
            # Store character in database (Tortoise ORM)
            character = await Character.create(
                channel_id="brainrot_grandfather",
                character_name="Grandfather",
                image_path=file_path,
                metadata={"type": "grandfather"}
            )
            
            logger.info(f"✅ Grandfather character stored: {character.id}")
            return file_path
        except Exception as e:
            logger.error(f"❌ Failed to store character: {e}")
            raise
    
    async def get_character(self, channel_id: str) -> Character:
        """Get character for channel."""
        try:
            character = await Character.get_or_none(channel_id=channel_id)
            return character
        except Exception as e:
            logger.error(f"❌ Failed to get character: {e}")
            raise


def get_character_service() -> CharacterService:
    """Get character service instance."""
    return CharacterService()
