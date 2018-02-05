# coding: utf-8

import logging
from logging.handlers import RotatingFileHandler

from base.config.config import Config
from base.tools.sm_tools import SmallTools


class Log4Kissenium:
    def __init__(self):
        self.config = Config()

    def setup(self, name, path):
        """
        Every log file will be created in "reports/" folder.
        :param name: Filename of the log
        :param path: Relative path of the log
        :return: logger
        """
        final_path = SmallTools.get_reports_folder(path)

        logger = logging.getLogger(name)
        logger.setLevel(self.get_log_level())
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler(final_path + name + '.log', 'a', 1000000, 1)
        file_handler.setLevel(self.get_log_level())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def get_log_level(self):
        if self.config.get_log_level() == "DEBUG":
            log_level = logging.DEBUG
        elif self.config.get_log_level() == "INFO":
            log_level = logging.INFO
        elif self.config.get_log_level() == "WARNING":
            log_level = logging.WARNING
        elif self.config.get_log_level() == "ERROR":
            log_level = logging.ERROR
        else:
            log_level = logging.DEBUG
        return log_level

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
