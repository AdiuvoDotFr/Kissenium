# coding: utf-8

from base.tools.js_tools import JsTools
from base.tools.platform import Platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from base.config.config import Config
from selenium.webdriver.common.action_chains import ActionChains


class Selenium():
    """
        Get the desired browser
    """

    def __init__(self, logger, screenshot):
        self.screenshot = screenshot
        self.logger = logger
        self.config = Config()
        self.browser = Platform.get_webdriver(self.config.get_browser())
        self.browser.switch_to_window(self.browser.current_window_handle)
        self.js = JsTools(self.config.get_message_status(), self.config.get_dim_status(), self.logger, self.config.get_page_wait())

        if self.config.get_browser_size() == "Maximize":
            self.maximize()
        else:
            width, height = self.config.get_browser_size().split('*')
            self.resize_window(width, height)


    def __handle_exception(self, message):
        """
        Handle Selennium exception
        :return: Nothing
        """
        self.logger.error(message)
        if self.config.get_capture_on_fail() == "True":
            self.screenshot.capture(self.browser, message)
        if self.config.get_fail_on_error() == "True":
            raise Exception(message)
        return False

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

    def alert(self, message, duration, pause):
        self.js.message(self.browser, message, duration, pause)

    def dim(self, id, duration):
        self.js.dim_by_id(self.browser, id, duration)

    def quit(self):
        self.browser.quit()

    def get(self, url):
        try:
            self.browser.get(url)
        except Exception as e:
            self.__handle_exception("[page_wait] Error : %s" % e)

    def page_wait(self, by_type, element):
        try:
            WebDriverWait(self.browser, int(self.config.get_page_wait())).until(
                ec.presence_of_element_located((By.__dict__.get(by_type), element))
            )
            self.logger.info("[page_wait] Page loaded")
            return True
        except TimeoutException as e:
            self.logger.error("[page_wait] TimeoutException error : %s" % e)
            return False
        except Exception as e:
            self.__handle_exception("[page_wait] Error : %s" % e)

    def page_wait_for_id(self, element):
        self.page_wait('ID', element)

    def page_wait_for_xpath(self, element):
        self.page_wait('XPATH', element)

    def test_element(self, by_type, path):
        try:
            self.browser.find_element(By.__dict__.get(by_type), value=path)
            self.logger.info("[test_element] Success : %s -- %s " % (type, path))
            return True
        except Exception as e:
            self.__handle_exception("[test_element] ERROR : %s" % e)

    def get_element(self, by_type, path):
        try:
            el = self.browser.find_element(By.__dict__.get(by_type), path)
            self.logger.info("[get_element] Success : %s -- %s " % (by_type, path))
            return el
        except Exception as e:
            self.__handle_exception("[get_element] By %s : Exception : %s" % (by_type, e))

    def get_elements(self, by_type, path):
        try:
            el = self.browser.find_elements(By.__dict__.get(by_type), path)
            self.logger.info("[get_elements] Success : %s -- %s " % (by_type, path))
            return el
        except Exception as e:
            self.__handle_exception("[get_elements] By %s : Exception : %s" % (by_type, e))

    def get_element_by_xpath(self, xpath):
        try:
            return self.get_element("XPATH", xpath)
        except Exception as e:
            self.__handle_exception("[get_element_by_xpath] Exception : %s" % e)

    def get_element_by_id(self, id):
        try:
            return self.get_element("ID", id)
        except Exception as e:
            self.__handle_exception("[get_element_by_id] Exception : %s" % e)

    def get_element_text_by_xpath(self, xpath):
        try:
            return self.get_element_text_by_xpath(xpath).text
        except Exception as e:
            self.__handle_exception("[get_element_by_xpath] Exception : %s" % e)

    def get_elements_by_xpath(self, xpath):
        try:
            return self.get_elements("XPATH", xpath)
        except Exception as e:
            self.__handle_exception("[get_elements_by_xpath] ERROR : %s" % e)

    def get_first_element_by_xpath(self, xpath):
        try:
            el = self.get_elements_by_xpath(xpath)
            for e in el:
                self.logger.debug(e.text)
            self.logger.info("[get_first_element_by_xpath] Success : %s " % xpath)
            return el[0]
        except Exception as e:
            self.__handle_exception("[get_first_element_by_xpath] ERROR : %s" % e)

    def click_first_xpath(self, xpath):
        try:
            el = self.get_first_element_by_xpath(xpath)
            el.click()
            self.logger.info("[click_first_xpath] Success : %s " % xpath)
        except Exception as e:
            self.__handle_exception("[click_first_xpath] ERROR : %s" % e)

    def click_id(self, id):
        try:
            self.get_element_by_id(id).click()
            self.logger.info("[click_first_xpath] Success : %s " % id)
        except Exception as e:
            self.__handle_exception("[click_id] ERROR : %s" % e)

    def close_tab(self):
        try:
            self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
            self.logger.info("[close_tab] Success")
        except Exception as e:
            self.__handle_exception("[close_tab] ERROR : %s" % e)

    def hover_by_xpath(self, xpath):
        try:
            element_to_hover_over = self.browser.find_element_by_xpath(xpath)
            ActionChains(self.browser).move_to_element(element_to_hover_over).perform()
            self.logger.info("[hover_by_xpath] Success")
        except Exception as e:
            self.__handle_exception("[hover_by_xpath] ERROR : %s" % e)
