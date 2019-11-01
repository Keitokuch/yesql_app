import logging


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG,  # lowest level to show in console
    filename="logs/logs.txt"
)

logger = logging.getLogger(__name__)

logger.info("new info")
