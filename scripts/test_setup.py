"""Test setup iniziale."""
import asyncio
from flux_agent.config import settings
from flux_agent.logging_config import logger
from flux_agent.storage import db


async def main():
    # Test config
    logger.info(f"LMStudio URL: {settings.lmstudio_url}")
    logger.info(f"Database path: {settings.database_path}")
    
    # Test database
    await db.initialize()
    logger.info("✅ Setup completato!")


if __name__ == "__main__":
    asyncio.run(main())