# coding: utf-8

"""
Base test module, holding the BaseTest class
"""

import unittest
from base.capture.screenshot import Screenshot
from base.config.config import Config
from base.logs.log import Log4Kissenium
from base.selenium.selenium import Selenium
from base.reports.decorators import assertion_error


class BaseTest(unittest.TestCase):
    """
        In this base class we will redefine some asserts tests to be sure that we have sufficient
        logs in the test reports folders.
        We do not modify the asserts tests, we just had logs where we want to and a status report.
        Be sure to refer to this url if you want to had a new one :
            https://docs.python.org/3/library/unittest.html
    """

    def self_setup(self):
        """
        This is the setup class
        :return:
        """
        self.has_error = False
        self.logger = self.get_logger()
        self.config = Config()
        self.screenshot = Screenshot(self.__class__.__name__, self._testMethodName)
        self.selenium = Selenium(self.logger, self.screenshot)
        self.browser = self.selenium.browser


    def self_teardown(self):
        """
        This is the teardown class
        :return:
        """
        self.selenium.quit()
        self.logger.info("End of %s - %s Test" % (self.__class__.__name__, self._testMethodName))

    def get_logger(self):
        """
        For internal class use only, get the logger
        :return: Log4Kissenium
        """
        logger = Log4Kissenium().setup(self._testMethodName, self.__class__.__name__)
        logger.info("Starting %s-%s Test", self.__class__.__name__, self._testMethodName)
        return logger

    def take_capture(self, suffix=''):
        """
        Take a capture of the running test.
        Configuration come from kissenium.ini (CaptureSize : Full | Browser)
        :return: Nothing
        """
        self.screenshot.capture(self.selenium.browser, suffix)

    def take_assert_capture(self, suffix=''):
        """
        Take a capture of the failing assert moment.
        Configuration come from kissenium.ini (CaptureOnAssertFail : True | False)
        :return: Nothing
        """
        if self.config.get_capture_on_assert_fail() == 'True':
            self.take_capture(suffix)

    @assertion_error()
    def l_assertEqual(self, a, b, stop_on_fail=None):
        """
        Test if a is equal to b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertEqual(a, b)
        self.logger.info("AssertEqual : %s is equal to %s", a, b)

    @assertion_error()
    def l_assertNotEqual(self, a, b, stop_on_fail=None):
        """
        Test if a is True, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertNotEqual(a, b)
        self.logger.info("AssertNotEqual : %s is not equal to %s", a, b)

    @assertion_error()
    def l_assertTrue(self, a, stop_on_fail=None):
        """
        Test if a is equal to b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertTrue(a)
        self.logger.info("AssertTrue : %s is True", a)

    @assertion_error()
    def l_assertFalse(self, a, stop_on_fail=None):
        """
        Test if a is False, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertFalse(a)
        self.logger.info("AssertFalse : %s is False", a)

    @assertion_error()
    def l_assertIsNone(self, a, stop_on_fail=None):
        """
        Test if a is None, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertIsNone(a)
        self.logger.info("AssertIsNone : %s is None", a)

    @assertion_error()
    def l_assertIsNotNone(self, a, stop_on_fail=None):
        """
        Test if a is not None, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertIsNotNone(a)
        self.logger.info("AssertIsNotNone : %s is not None", a)

    @assertion_error()
    def l_assertIn(self, a, b, stop_on_fail=None):
        """
        Test if a is in b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertIn(a, b)

    @assertion_error()
    def l_assertNotIn(self, a, b, stop_on_fail=None):
        """
        Test if a is not in b, standard assert test but with log and status report
        stop_on_fail will override FailOnAssertError from kissenium.ini.
        :param a: First parameter
        :param b: Second parameter
        :param stop_on_fail: True | False
        :return: Nothing
        """
        self.assertNotIn(a, b)
        self.logger.info("AssertNotIn : %s is not in %s", a, b)
