import logging
import os

logger = logging.getLogger("open-crawler")
logger.setLevel(
    logging.getLevelName(os.environ.get("LOGGER_LEVEL", "INFO").upper())
)
