# coding: utf-8

"""
Module screenshot: take a screenshot of the full scren or the browser
"""

import mss
from PIL import Image

from base.config.config import Config
from base.tools.sm_tools import SmallTools


class Screenshot:
    """
    Class used to take screenshot of the full screen or the browser only
    """
    scenario = ""

    def __init__(self, scenario, test):
        """
        Initializing the Screenshot class
        :param scenario: Scenario name
        :param test: Test name
        """
        self.scenario = scenario
        self.test = test
        self.cancelled = False
        self.config = Config()
        self.reports_folder = SmallTools.get_reports_folder(self.scenario)

    def capture(self, browser, suffix=''):
        """
        Capture the current test
        :param browser: Selenium instance
        :param suffix: Suffix to put to filename
        :return:
        """
        if suffix != '':
            suffix = '-' + suffix
        filename = SmallTools.sanitize_filename('%s%s.png' % (self.test, suffix))

        if self.config.get_capture_size() == 'Full':
            self.capture_screen(filename)
        else:
            self.capture_browser(browser, filename)

    def capture_screen(self, filename):
        """
        Capture the current screen (full capture)
        :param filename: Filename to use
        :return:
        """
        with mss.mss() as sct:
            sct.shot(output=self.reports_folder + filename)

    def capture_browser(self, browser, filename):
        """
        Capture the test inside the brpwser
        :param browser: Selenium instance
        :param filename: Filename to use
        :return:
        """
        reports_folder = SmallTools.get_reports_folder(self.scenario)
        browser.get_screenshot_as_file(reports_folder + filename)
