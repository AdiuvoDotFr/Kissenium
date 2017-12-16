#!/usr/bin/env python3
# coding: utf-8

import os
import glob
import time
import unittest
import configparser
import logging
from base.log import Log4Kissenium
from base.config import Config
from base.sm_tools import SmallTools
from base.capture.screenshot import Screenshot
from base.capture.record import Record


class KisseniumUnitTests(unittest.TestCase):
    """Tests for Kissenium."""

    def setUp(self):
        reports_list = glob.glob("reports/*")
        globs = [reports_list]
        for g in globs:
            SmallTools.delete_from_glob(g)
        SmallTools.check_path("reports/tmp")

    def test_config_reader(self):
        config = Config()
        self.assertEqual("Chrome", config.get_browser())

        #Test fallback value
        new_config = configparser.ConfigParser()
        new_config.read('kissenium.ini')
        config_ref = configparser.ConfigParser()
        config_ref.read('kissenium.ini')

        new_config.remove_option('Kissenium', 'Browser')
        with open('kissenium.ini', 'w') as f:
            new_config.write(f)

        config = Config()
        self.assertEqual("Chrome", config.get_browser())

        #Resetting ini file values
        with open('kissenium.ini', 'w') as f:
            config_ref.write(f)


    def test_logger(self):
        """Test the logger functions"""
        #Setup the logger
        logger = Log4Kissenium().setup(self._testMethodName, self.__class__.__name__)
        message = 'Test of logger write to file'
        logger.debug(message)
        r = SmallTools.get_lines_from_file('reports/' + self.__class__.__name__ + '/', self._testMethodName + '.log')
        self.assertIn(message, r[-1])

        #Test the get logger
        second_logger = Log4Kissenium().get_logger(self._testMethodName)
        message = "Test the get logger function"
        second_logger.info(message)
        r = SmallTools.get_lines_from_file('reports/' + self.__class__.__name__ + '/', self._testMethodName + '.log')
        self.assertIn(message, r[-1])

    def test_screenshot(self):
        screenshot = Screenshot(self.__class__.__name__, self._testMethodName)
        screenshot.capture(None, '')
        self.assertTrue(os.path.isfile('reports/' + self.__class__.__name__ + '/' + self._testMethodName + '.png'))

    def test_recordscreen(self):
        recorder = Record(self.__class__.__name__, self._testMethodName)
        recorder.start()
        time.sleep(5)
        recorder.stop()
        time.sleep(2)
        self.assertTrue(os.path.isfile('reports/' + self.__class__.__name__ + '/' + self._testMethodName + '.avi'))
