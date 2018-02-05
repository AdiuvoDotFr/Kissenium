# coding: utf-8
# pylint: disable=R0904

"""Selenium Module
Here we will define all methods used in the web browser.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from base.reports.decorators import exception
from base.tools.js_tools import JsTools
from base.tools.platform import Platform
from base.config.config import Config


class Selenium:
    """Selenium class to use Selenium webdriver or marionette
    This class is intented to surround every selenium call with a maximum of reporting in case of
    error
    """

    def __init__(self, logger, screenshot):
        self.screenshot = screenshot
        self.logger = logger
        self.config = Config()
        self.browser = Platform.get_webdriver(self.config.get_browser())
        self.browser.switch_to_window(self.browser.current_window_handle)
        self.js = JsTools(self.config.get_message_status(), self.config.get_dim_status(),
                          self.logger, self.config.get_page_wait())

        if self.config.get_browser_size() == "Maximize":
            self.maximize()
        else:
            width, height = self.config.get_browser_size().split('*')
            self.resize_window(width, height)

    def __handle_exception(self, message):
        """Handle Selennium exception
        """
        self.logger.error(message)
        if self.config.get_capture_on_fail() == "True":
            self.screenshot.capture(self.browser, message)
        if self.config.get_fail_on_error() == "True":
            raise Exception(message)
        return False

    def maximize(self):
        """Maximize browser window
        """
        self.browser.maximize_window()
        self.logger.info("Browser window has been maximized.")

    def resize_window(self, width, height):
        """Resize browser window to width and height

        :param width: Int
        :param height: Int
        """
        self.browser.set_window_size(width, height)
        self.logger.info("Browser window has been resized to : %s x %s." % (width, height))

    def alert(self, message, duration, pause):
        """Display a message into the browser (if activated in kissenium.ini file)

        :param message: Your message
        :param duration: Duration of the display
        :param pause: Time while nothing will be done
        """
        self.js.message(self.browser, message, duration, pause)

    def dim(self, e_id, duration):
        """Dimming the page to get one element lighter

        :param e_id: The id of the element
        :param duration: Duration of the dimming
        """
        self.js.dim_by_id(self.browser, e_id, duration)

    def quit(self):
        """Quitting the browser
        """
        self.browser.quit()

    @exception("Error getting the url")
    def get(self, url):
        """Get one url into the browser

        :param url:
        """
        self.browser.get(url)

    def page_wait(self, by_type, element):
        """Wait for one element to be present in the web page, and block execution while not present

        :param by_type:
        :param element:
        """
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
        """Wait for id to be present in the page

        :param element:
        """
        self.page_wait('ID', element)

    def page_wait_for_xpath(self, element):
        """Wait for xpath to be present in the webpage

        :param element:
        """
        self.page_wait('XPATH', element)

    @exception("Error testing the element")
    def test_element(self, by_type, path):
        """Test if the element is present in the page

        :param by_type:
        :param path:
        :return: Boolean
        """
        self.browser.find_element(By.__dict__.get(by_type), value=path)
        self.logger.info("[test_element] Success : %s -- %s " % (type, path))
        return True

    def get_element(self, by_type, path):
        """Get element in page

        :param by_type:
        :param path:
        """
        try:
            el = self.browser.find_element(By.__dict__.get(by_type), path)
            self.logger.info("[get_element] Success : %s -- %s " % (by_type, path))
            return el
        except Exception as e:
            self.__handle_exception("[get_element] By %s : Exception : %s" % (by_type, e))

    def get_elements(self, by_type, path):
        """Get multiple elements by type

        :param by_type: Type of dom manipulation to use
        :param path: Path to use for the query
        """
        try:
            el = self.browser.find_elements(By.__dict__.get(by_type), path)
            self.logger.info("[get_elements] Success : %s -- %s " % (by_type, path))
            return el
        except Exception as e:
            self.__handle_exception("[get_elements] By %s : Exception : %s" % (by_type, e))

    @exception("Error getting the element by xpath")
    def get_element_by_xpath(self, xpath):
        """Get element by xpath

        :param xpath:
        """
        return self.get_element("XPATH", xpath)

    @exception("Error getting the element by id")
    def get_element_by_id(self, e_id):
        """Get element by id

        :param e_id:
        """
        return self.get_element("ID", e_id)

    @exception("Error getting the text element by xpath")
    def get_element_text_by_xpath(self, xpath):
        """Get element by xpath£*

        :param xpath:
        """
        return self.get_element_text_by_xpath(xpath).text

    @exception("Error getting the elements by xpath")
    def get_elements_by_xpath(self, xpath):
        """Get all elements corresponding to xpath

        :param xpath:
        """
        return self.get_elements("XPATH", xpath)

    @exception("Error getting the first element by xpath")
    def get_first_element_by_xpath(self, xpath):
        """Get first element corresponding to xpath

        :param xpath:
        """
        el = self.get_elements_by_xpath(xpath)
        for e in el:
            self.logger.debug(e.text)
        self.logger.info("[get_first_element_by_xpath] Success : %s " % xpath)
        return el[0]

    @exception("Error sending keys to element by id")
    def send_keys(self, element, keys):
        """Send keys to element

        :param element: Element to send keys
        :param keys: Keys to send
        """
        element.send_keys(keys)
        self.logger.info("[send_keys] Success : %s " % keys)

    @exception("Error sending keys to element by id")
    def send_keys_by_id(self, e_id, keys):
        """Find element by id and send keys to it

        :param e_id: Element id
        :param keys: Keys to send
        """
        e = self.get_element_by_id(e_id)
        self.send_keys(e, keys)
        self.logger.info("[send_keys_by_id] Success : %s " % e_id)

    @exception("Error sending keys to element by xpath")
    def send_keys_by_xpath(self, xpath, keys):
        """Find element by xpath and send keys to it

        :param xpath: Xpath to find element
        :param keys: Keys to send
        """
        e = self.get_element_by_xpath(xpath)
        self.send_keys(e, keys)
        self.logger.info("[send_keys_by_id] Success : %s " % xpath)

    @exception("Error clicking the first element by xpath")
    def click_first_xpath(self, xpath):
        """Click first element finded by xpath

        :param xpath:
        """
        el = self.get_first_element_by_xpath(xpath)
        el.click()
        self.logger.info("[click_first_xpath] Success : %s " % xpath)

    @exception("Error clicking the element by id")
    def click_id(self, e_id):
        """Click element by id

        :param e_id:
        """
        self.get_element_by_id(e_id).click()
        self.logger.info("[click_first_xpath] Success : %s " % e_id)

    @exception("Error closing the tab")
    def close_tab(self):
        """Close the browser tab
        """
        self.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
        self.logger.info("[close_tab] Success")

    @exception()
    def scroll_to_xpath(self, xpath):
        """Hover one element with xpath

        :param xpath: xpath element to find
        """
        self.page_wait_for_xpath(xpath)
        element_to_hover = self.browser.find_element_by_xpath(xpath)
        self.browser.execute_script("arguments[0].scrollIntoView();", element_to_hover)
        self.logger.info("[hover_by_xpath] Success")

    @exception()
    def scroll_to_id(self, e_id):
        """Hover one element with xpath

        :param xpath: xpath element to find
        """
        self.page_wait_for_id(e_id)
        element_to_hover = self.browser.find_element_by_id(e_id)
        self.browser.execute_script("arguments[0].scrollIntoView();", element_to_hover)
        self.logger.info("[hover_by_xpath] Success")

    @exception()
    def scroll_to_element(self, e):
        """Hover one element

        :param xpath: xpath element to find
        """
        self.browser.execute_script("arguments[0].scrollIntoView();", e)
        self.logger.info("[scroll_to_element] Success")

    @exception()
    def move_cursor_to(self, xpath):
        """Hover one element with xpath

        :param xpath: xpath element to find
        """
        self.page_wait_for_xpath(xpath)
        element_to_hover = self.browser.find_element_by_xpath(xpath)
        ActionChains(self.browser).move_to_element(element_to_hover).perform()
        self.logger.info("[move_cursor_to] Success")
