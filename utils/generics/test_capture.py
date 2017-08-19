# coding: utf-8
from selenium import webdriver
from utils.sm_tools import SmallTools
from selenium.webdriver.common.action_chains import ActionChains
from utils.generics import BaseTest


class GenericTestCapture(BaseTest):

    def setUp(self):
        self.has_error = False
        self.get_logger()
        self.get_config()
        self.get_capture_handler()
        self.browser = webdriver.Firefox(log_path='reports/Kissenium/geckodriver.log')
        self.actionChains = ActionChains(self.browser)

    def tearDown(self):
        if self.has_error:
            self.take_capture()
        self.browser.quit()
        self.logger.info("End of %s-%s Test" % (self.__class__.__name__, self._testMethodName))
