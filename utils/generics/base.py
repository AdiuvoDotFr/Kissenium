# coding: utf-8
import unittest
from utils.platform import Platform
from utils.log import Log4Kissenium
from utils.config import Config
from utils.screen_capture import ScreenCapture
from selenium.webdriver.common.action_chains import ActionChains
from utils.selenium_toolbox import SeleniumToolBox
from utils.js_tools import JsTools


class BaseTest(unittest.TestCase):
    """
        In this base class we will redefine some asserts tests to be sure that we have sufficient logs in the test
        reports folders.
        We do not modify the asserts tests, we just had logs where we want to and a status report.
        Be sure to refer to this url if you want to had a new one : https://docs.python.org/3/library/unittest.html
    """

    def self_setup(self):
        self.has_error = False
        self.get_logger()
        self.get_config()
        self.get_capture_handler()
        self.browser = Platform.get_webdriver(self.config.get_browser())
        self.actionChains = ActionChains(self.browser)
        self.st = SeleniumToolBox(self.logger, self.screenshot)
        self.js = JsTools(self.config.get_message_status(), self.config.get_dim_status(), self.logger, self.config.get_page_wait())

        if self.config.get_browser_size() == "Maximize":
            self.maximize()
        else:
            width, height = self.config.get_browser_size().split('*')
            self.resize_window(width, height)



    def self_teardown(self):
        self.browser.quit()
        self.logger.info("End of %s - %s Test" % (self.__class__.__name__, self._testMethodName))

    def get_config(self):
        self.config = Config()

    def get_logger(self):
        """
        For internal class use only, get the logger
        :return: Nothing
        """
        self.logger = Log4Kissenium().setup(self._testMethodName, self.__class__.__name__)
        self.logger.info("Starting %s-%s Test" % (self.__class__.__name__, self._testMethodName))

    def get_capture_handler(self):
        """
        Get capture handler
        :return: Nothing
        """
        self.screenshot = ScreenCapture(self.__class__.__name__, self._testMethodName)

    def take_capture(self, suffix=''):
        """
        Take a capture of the running test.
        Configuration come from kissenium.ini (CaptureSize : Full | Browser)
        :return: Nothing
        """
        self.screenshot.capture(self.browser, suffix)

    def take_assert_capture(self, suffix=''):
        """
        Take a capture of the failing assert moment.
        Configuration come from kissenium.ini (CaptureOnAssertFail : True | False)
        :return: Nothing
        """
        if self.config.get_capture_on_assert_fail() == 'True':
            self.take_capture(suffix)

    def assert_error_handler(self, message, stop_on_fail=None):
        """
        Taking care of the action after detection of an assert error
        :param message: Error message
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.logger.error(message)
        self.has_error = True
        self.take_assert_capture(suffix=message)

        if stop_on_fail is True:
            raise AssertionError(message)
        elif stop_on_fail is not None and stop_on_fail is False:
            return
        elif not self.config.get_fail_on_assert_error() == 'False':
            raise AssertionError(message)

    def l_assertEqual(self, a, b, stop_on_fail=None):
        """
        Test if a is equal to b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertEqual(a, b)
            self.logger.info("AssertEqual : %s is equal to %s" % (a, b))
        except AssertionError:
            self.assert_error_handler("AssertEqual : %s is NOT equal to %s" % (a, b), stop_on_fail)

    def l_assertNotEqual(self, a, b, stop_on_fail=None):
        """
        Test if a is True, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertNotEqual(a, b)
            self.logger.info("AssertNotEqual : %s is not equal to %s" % (a, b))
        except AssertionError:
            self.assert_error_handler("AssertNotEqual : %s IS equal to %s" % (a, b), stop_on_fail)

    def l_assertTrue(self, a, stop_on_fail=None):
        """
        Test if a is equal to b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertTrue(a)
            self.logger.info("AssertTrue : %s is True" % a)
        except AssertionError:
            self.assert_error_handler("AssertTrue : %s is FALSE" % a, stop_on_fail)

    def l_assertFalse(self, a, stop_on_fail=None):
        """
        Test if a is False, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertFalse(a)
            self.logger.info("AssertFalse : %s is False" % a)
        except AssertionError:
            self.assert_error_handler("AssertFalse : %s is TRUE" % a, stop_on_fail)

    def l_assertIsNone(self, a, stop_on_fail=None):
        """
        Test if a is None, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertIsNone(a)
            self.logger.info("AssertIsNone : %s is None" % a)
        except AssertionError:
            self.assert_error_handler("AssertIsNone : %s is NOT None" % a, stop_on_fail)

    def l_assertIsNotNone(self, a, stop_on_fail=None):
        """
        Test if a is not None, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertIsNotNone(a)
            self.logger.info("AssertIsNotNone : %s is not None" % a)
        except AssertionError:
            self.assert_error_handler("AssertIsNotNone : %s IS None" % a, stop_on_fail)

    def l_assertIn(self, a, b, stop_on_fail=None):
        """
        Test if a is in b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertIn(a, b)
            self.logger.info("AssertIn : %s is in %s" % (a, b))
        except AssertionError:
            self.assert_error_handler("AssertIn : %s is NOT in %s" % (a, b), stop_on_fail)

    def l_assertNotIn(self, a, b, stop_on_fail=None):
        """
        Test if a is not in b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        try:
            self.assertNotIn(a, b)
            self.logger.info("AssertNotIn : %s is not in %s" % (a, b))
        except AssertionError:
            self.assert_error_handler("AssertNotIn : %s IS in %s" % (a, b), stop_on_fail)

    def maximize(self):
        """
        Maximize browser window
        :return: Nothing
        """
        self.browser.maximize_window()
        self.logger.info("Browser window has been maximized.")

    def resize_window(self, width, height):
        """
        Resize browser window to width and height
        :param width: Int
        :param height: Int
        :return: Nothing
        """
        self.browser.set_window_size(width, height)
        self.logger.info("Browser window has been resized to : %s x %s." % (width, height))

