# coding: utf-8
import os
from base.log import Log4Kissenium
from sys import platform
import struct
from selenium import webdriver


class Platform:

    @staticmethod
    def get_os():
        if platform == "linux" or platform == "linux32":
            return "linux"
        elif platform == "darwin":
            return "mac"
        elif platform == "win32":
            return "win"

    @staticmethod
    def get_arch():
        if struct.calcsize('P') * 8 == 64:
            return "amd64"
        else:
            return "i386"

    @staticmethod
    def get_webdriver(browser):
        # TODO Finish this function
        logger = Log4Kissenium.get_logger("Kissenium")
        os_name = Platform.get_os()
        os_arch = Platform.get_arch()

        logger.debug("Os type is %s and architecture is %s" % (os_name, os_arch))

        if browser == "Chrome":
            chromedriver = "%s/resources/webdriver/chrome/%s/%s/chromedriver" % (os.getcwd(), os_name, os_arch)
            os.environ["webdriver.chrome.driver"] = chromedriver
            return webdriver.Chrome(chromedriver)
        else:
            geckodriver = "%s/resources/webdriver/firefox/%s/%s/geckodriver" % (os.getcwd(), os_name, os_arch)
            logger.debug(geckodriver)
            return webdriver.Firefox(log_path='reports/Kissenium/geckodriver.log', executable_path=geckodriver)
