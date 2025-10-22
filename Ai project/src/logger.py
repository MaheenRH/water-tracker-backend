import logging
from datetime import datetime
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logger
LOG_FILE = f"logs/water_tracker_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("water_tracker")

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)
