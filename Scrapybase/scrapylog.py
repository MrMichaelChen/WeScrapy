# encoding=utf-8
import ConfigParser
import os
import logging

if os._exists('Scrapyconfig/logging.conf'):
    logging.config.fileConfig('Scrapyconfig/logging.conf')
else:
    import logging
    import re
    from logging.handlers import TimedRotatingFileHandler

    log_fmt = '%(asctime)s\t%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    log_file_handler = TimedRotatingFileHandler(
        filename="../log/logging.log",
        when="midnight",
        interval=1,
        backupCount=3)
    log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
    log_file_handler.extMatch = re.compile(
        r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.DEBUG)
    logger = logging.getLogger()
    logger.addHandler(log_file_handler)
    logger.setLevel(logging.NOTSET)

logger = logging.getLogger('debugLogger')
