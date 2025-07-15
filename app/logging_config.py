import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists("app/data/logs"):
    os.mkdir("app/data/logs")

# Set up file handler with rotation
file_handler = RotatingFileHandler(
    filename="app/data/logs/app.log",
    maxBytes=1_048 * 1024 * 10,  # 10 MB
    backupCount=3
)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
)
file_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # console
        file_handler              # file
    ]
)

logger = logging.getLogger(__name__)
logger.info("Logging is set up.")