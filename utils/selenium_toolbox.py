# coding: utf-8
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.config import Config


class SeleniumToolBox:

    def __init__(self, logger, screenshot):
        self.logger = logger
        self.screenshot = screenshot
        self.config = Config()

    def handle_exception(self, browser, message):
        self.logger.error(message)
        if self.config.get_capture_on_fail() == "True":
            self.screenshot.capture(browser, message)
        if self.config.get_fail_on_error() == "True":
            raise Exception(message)
        return False

    def page_wait(self, browser, by_type, element):
        try:
            WebDriverWait(browser, int(self.config.get_page_wait())).until(
                ec.presence_of_element_located((By.__dict__.get(by_type), element))
            )
            self.logger.info("[page_wait] Page loaded")
            return True
        except TimeoutException as e:
            self.logger.error("[page_wait] TimeoutException error : %s" % e)
            return False
        except Exception as e:
            self.handle_exception(browser, "[page_wait] Error : %s" % e)

    def page_wait_for_id(self, browser, element):
        self.page_wait(browser, 'ID', element)

    def page_wait_for_xpath(self, browser, element):
        self.page_wait(browser, 'XPATH', element)

    def test_element(self, browser, by_type, path):
        try:
            browser.find_element(By.__dict__.get(by_type), value=path)
            self.logger.info("[test_element] Success : %s -- %s " % (type, path))
            return True
        except Exception as e:
            self.handle_exception(browser, "[test_element] ERROR : %s" % e)

    def get_element(self, browser, by_type, path):
        try:
            el = browser.find_element(By.__dict__.get(by_type), path)
            self.logger.info("[get_element] Success : %s -- %s " % (by_type, path))
            return el
        except Exception as e:
            self.handle_exception(browser, "[get_element] By %s : Exception : %s" % (by_type, e))

    def get_elements(self, browser, by_type, path):
        try:
            el = browser.find_elements(By.__dict__.get(by_type), path)
            self.logger.info("[get_elements] Success : %s -- %s " % (by_type, path))
            return el
        except Exception as e:
            self.handle_exception(browser, "[get_elements] By %s : Exception : %s" % (by_type, e))

    def get_element_by_xpath(self, browser, xpath):
        try:
            return self.get_element(browser, "XPATH", xpath)
        except Exception as e:
            self.handle_exception(browser, "[get_element_by_xpath] Exception : %s" % e)

    def get_element_by_id(self, browser, id):
        try:
            return self.get_element(browser, "ID", id)
        except Exception as e:
            self.handle_exception(browser, "[get_element_by_id] Exception : %s" % e)

    def get_element_text_by_xpath(self, browser, xpath):
        try:
            return self.get_element_text_by_xpath(browser, xpath).text
        except Exception as e:
            self.handle_exception(browser, "[get_element_by_xpath] Exception : %s" % e)

    def get_elements_by_xpath(self, browser, xpath):
        try:
            return self.get_elements(browser, "XPATH", xpath)
        except Exception as e:
            self.handle_exception(browser, "[get_elements_by_xpath] ERROR : %s" % e)

    def get_first_element_by_xpath(self, browser, xpath):
        try:
            el = self.get_elements_by_xpath(browser, xpath)
            for e in el:
                self.logger.debug(e.text)
            self.logger.info("[get_first_element_by_xpath] Success : %s " % xpath)
            return el[0]
        except Exception as e:
            self.handle_exception(browser, "[get_first_element_by_xpath] ERROR : %s" % e)

    def click_first_xpath(self, browser, xpath):
        try:
            el = self.get_first_element_by_xpath(browser, xpath)
            el.click()
            self.logger.info("[click_first_xpath] Success : %s " % xpath)
        except Exception as e:
            self.handle_exception(browser, "[click_first_xpath] ERROR : %s" % e)

    def click_id(self, browser, id):
        try:
            self.get_element_by_id(browser, id).click()
            self.logger.info("[click_first_xpath] Success : %s " % id)
        except Exception as e:
            self.handle_exception(browser, "[click_id] ERROR : %s" % e)

    def close_tab(self, browser):
        try:
            browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
            self.logger.info("[close_tab] Success")
        except Exception as e:
            self.handle_exception(browser, "[close_tab] ERROR : %s" % e)
