"""Configurazione logging."""
import logging
import sys
from flux_agent.config import settings

def setup_logging() -> logging.Logger:
    """Configura e ritorna il logger principale."""
    logger = logging.getLogger("flux_agent")
    logger.setLevel(settings.log_level)

    # Handler per console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.log_level)

    # Formato log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# Logger globale
logger = setup_logging()