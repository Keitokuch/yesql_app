import logging
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

LOG_LEVEL = logging.INFO

LOG_DIR = ROOT_DIR / "log"

LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = {
    'fmt': "%(asctime)s %(levelname)-8s %(message)s",
    'datefmt': "%Y-%m-%d %H:%M:%S"
}

LOG_SIZE = 5000000

LOG_CNT = 5

LOCAL_DIR = ROOT_DIR / "local"
