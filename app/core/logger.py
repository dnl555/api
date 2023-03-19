import logging
from app.core.config import log_level

logger = logging.getLogger("fastapi")


def get_handler():
    handler = logging.StreamHandler()
    return handler


def setup_logging():
    logger.setLevel(log_level)
    handler = get_handler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
