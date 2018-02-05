# coding: utf-8

"""Module screenshot: take a screenshot of the full scren or the browser
"""

import mss
from PIL import Image

from base.config.config import Config
from base.tools.sm_tools import SmallTools


class Screenshot:
    """Class used to take screenshot of the full screen or the browser only
    """
    scenario = ""

    def __init__(self, scenario, test):
        """Initializing the Screenshot class.

        Args:
            scenario (str): Scenario name.
            test (str): Test name.

        """
        self.scenario = scenario
        self.test = test
        self.cancelled = False
        self.config = Config()
        self.reports_folder = SmallTools.get_reports_folder(self.scenario)

    def capture(self, browser, suffix=''):
        """Capture the current test.

            :param browser: Selenium instance.
            :param suffix: Suffix to put to filename.
        """
        if suffix != '':
            suffix = '-' + suffix
        filename = SmallTools.sanitize_filename('%s%s.png' % (self.test, suffix))

        if self.config.get_capture_size() == 'Full':
            self.capture_screen(filename)
        else:
            self.capture_browser(browser, filename)

    def capture_screen(self, filename):
        """Capture the current screen (full capture)

        :param filename: Filename to use

        """
        with mss.mss() as sct:
            sct_img = sct.grab(sct.monitors[1])
            img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
            img = img.convert('RGB')
            output = self.reports_folder + filename
            img.save(output)

    def capture_browser(self, browser, filename):
        """Capture the test inside the browser

        :param browser: Selenium instance
        :param filename: Filename to use

        """
        reports_folder = SmallTools.get_reports_folder(self.scenario)
        browser.get_screenshot_as_file(reports_folder + filename)
