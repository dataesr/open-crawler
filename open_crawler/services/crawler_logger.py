import logging
import os

logger = logging.getLogger("open-crawler")
logger.setLevel(os.environ.get("LOGGER_LEVEL", "info"))
