# coding: utf-8
from utils.screen_recorder import ScreenRecorder
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from utils.generics import BaseTest


class GenericTestVideo(BaseTest):

    def setUp(self):
        """
        If you just want to use the main logger, get it like this
            self.logger = logging.getLogger("selenium")
        """
        self.has_error = False
        self.get_logger()
        self.get_config()
        self.get_capture_handler()
        self.recorder = ScreenRecorder(self.__class__.__name__, self._testMethodName)
        self.recorder.start()
        self.browser = webdriver.Firefox(log_path='reports/Kissenium/geckodriver.log')
        self.actionChains = ActionChains(self.browser)

    def tearDown(self):
        self.browser.quit()
        self.recorder.stop()
        self.recorder.generate_video()
        self.recorder.clean_captures()
        self.logger.info("End of %s-%s Test" % (self.__class__.__name__, self._testMethodName))
