import logging
import logging.handlers
import os
import utils.config as config


os.makedirs(config.LOG_DIR, exist_ok=True)
formatter = logging.Formatter(**config.LOG_FORMAT)
file_handler = logging.handlers.RotatingFileHandler(config.LOG_FILE,
                                                    maxBytes=config.LOG_SIZE,
                                                    backupCount=config.LOG_CNT)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(file_handler)
logger = logging.getLogger(__name__)
logger.info('log test 2')
"""
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
    logging.basicConfig(level=logging.INFO, filename=LOG_FILE, format=LOG_FORMAT)
    logging.info("\n\n-------------------- start -----------------------\n")
    logging.basicConfig(
        format=LOG_FORMAT,
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG,  # lowest level to show in console
        filename="logs/logs.txt"
    )

logger = logging.getLogger(__name__)

logger.info("new info")
"""
