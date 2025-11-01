"""
Tortoise ORM Database Manager - ASYNC ONLY
"""

import logging
from tortoise import Tortoise
from app.db.tortoise_config import TORTOISE_ORM

logger = logging.getLogger(__name__)


async def init_db():
    """Initialize database and auto-create schemas."""
    try:
        logger.info("🔄 Initializing Tortoise ORM...")
        
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas(safe=True)  # ✅ Creates/updates tables
        
        logger.info("✅ Database initialized and schemas created!")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def close_db():
    """Close database connection."""
    try:
        logger.info("🛑 Closing database connection...")
        await Tortoise.close_connections()
        logger.info("✅ Database connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")


async def check_database_health() -> bool:
    """Check database connection health."""
    try:
        await Tortoise.get_connection("default").execute_query("SELECT 1")
        logger.debug("✅ Database health check passed")
        return True
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return False
