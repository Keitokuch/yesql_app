import logging
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

LOG_LEVEL = logging.DEBUG

LOG_DIR = ROOT_DIR / "log"

LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = {
    #'fmt': "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] - %(message)s",
    'fmt': "%(asctime)s %(levelname)-8s %(message)s",
    'datefmt': "%Y-%m-%d %H:%M:%S"
}

LOG_SIZE = 5000

LOG_CNT = 5
