import os
import logging
import logging.config

LOCAL_DIR = os.path.abspath(os.path.dirname(__file__))
LOGGER_CONFIG_FILE = os.path.join(LOCAL_DIR, 'logging.ini')

logging.config.fileConfig(LOGGER_CONFIG_FILE, disable_existing_loggers=False)
