import os
import json
from config import config


def prepare_files():
    '''
    Prepare default files
    '''
    if not os.path.exists(config.LOGS_DIR):
        os.makedirs(config.LOGS_DIR)

    with open(config.ERROR_LOG_FILE, 'a+'):
        ...

    if not os.path.exists(config.DATA_DIR):
        os.makedirs(config.DATA_DIR)

# Calling in file to prepare files and dirs before setupping logger
prepare_files()
