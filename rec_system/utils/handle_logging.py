import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from .handle_config import log_config


LOG_NAME = log_config['log_name']
LOG_DIR = log_config['log_dir']
LOG_FILENAME = log_config['log_dest']


def get_logger(name: str = LOG_NAME):

    logger = logging.getLogger(name)
    if not logger.handlers:

        # 1. setup console handler
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.stream.reconfigure(encoding="utf-8", errors="replace")
        console_handler.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))
        logger.addHandler(console_handler)

        # 2. setup file handler with rotation (max 5MB, keep 3 backup)
        os.makedirs(name=LOG_DIR, exist_ok=True)
        file_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=5242880, backupCount=3)
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))
        logger.addHandler(file_handler)

        logger.setLevel(level=logging.INFO)

    return logger

log = get_logger()