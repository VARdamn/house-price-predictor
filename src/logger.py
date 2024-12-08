import re
import sys

from loguru import logger

from config import config


def format_file(record, format_string):
    return format_string + record['extra'].get('end', '\n') + '{exception}'


def format_stdout(record, level_padding=7):
    level = record['level'].name.ljust(level_padding)
    time = record['time'].strftime('%H:%M:%S.%f')[:-4]
    message = record['message']
    exception = record['exception']
    formatted_message = f'<green>{time}</green> | <blue>{level}</blue> | <level>{message}</level>'
    return formatted_message + record['extra'].get('end', '\n') + (exception if exception else '')


def clean_brackets(raw_str):
    return re.sub(r'<.*?>', '', raw_str)


def setup_logger():
    format_error = (
        '<green>{time:HH:mm:ss.SS}</green> | <blue>{level}</blue> | '
        '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | '
        '<level>{message}</level>'
    )  # noqa

    logger.remove()

    logger.add(config.ERROR_LOG_FILE, colorize=False, format=lambda record: format_file(record, clean_brackets(format_error)), level='ERROR')
    logger.add(sys.stdout, colorize=True, format=lambda record: format_stdout(record), level='INFO')


setup_logger()
