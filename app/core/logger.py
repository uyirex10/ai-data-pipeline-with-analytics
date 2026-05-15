import logging
import os

from app.core.config import settings


LOG_DIRECTORY = "logs"

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)


LOG_FILE_PATH = os.path.join(LOG_DIRECTORY, "pipeline.log")


logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    ),
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(settings.APP_NAME)