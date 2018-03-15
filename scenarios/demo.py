# coding: utf-8

"""
Copyright 2017 Adiuvo

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from base.generics.test import GenericTest
import unittest
from selenium.webdriver.common.action_chains import ActionChains


class TestDemo(GenericTest):
    """This is a demo class who will show-up most of the functionalities of this small test environment.
    PLease check the kissenium.ini file for more configuration
    If you need to run your tests in a specific order, you can add an order number after the method keyword 'test'
    Like this:
        def test_4_test_name(self):
            # My test
    """

    @unittest.skip("This is an example of a skipped test.")
    def test_1_from_google_search(self):
        # Our first assert will be to check the google title
        self.selenium.get('https://www.google.fr')
        self.selenium.alert("This test will go trough standard browsing on the web with some tests.", 5, 3)
        self.l_assertIn('Google', self.selenium.browser.title, False)

        # We start by searching for selenium into google
        self.selenium.alert("We are starting by searching for selenium in google", 2, 1)
        self.selenium.send_keys_by_xpath("//input[@title='Rechercher']", "selenium software")
        self.selenium.get_element_by_xpath("//input[@value='Recherche Google']").click()

        # For the demo we will log every page name in the result of google
        self.selenium.alert("We can parse the google results", 10, 1)
        self.selenium.alert("Check the logs to see the results", 10, 1)
        for entry in self.selenium.get_elements_by_xpath('//div[@id="res"]//h3//a'):
            self.logger.info("Element iteration demo : " + entry.text)

        # We first go into wikipedia, run an assert, and then go back
        self.selenium.scroll_to_xpath("//a[contains(., 'Wikipédia')]")
        self.selenium.click_first_xpath("//a[contains(., 'Wikipédia')]")
        self.selenium.alert("Browsing wikipedia page", 2, 1)
        self.selenium.alert("Testing the page title", 2, 1)
        title = self.selenium.get_element_by_id('firstHeading')
        self.l_assertIn("Selenium", title.text)
        self.selenium.alert("Page title is ok!", 2, 1)
        self.selenium.alert("Go to the previous page (self.browser.page)", 1, 1)
        self.selenium.browser.back()

        # We are going to the selenium official website
        self.selenium.alert("Go to the selenium website", 2, 2)
        self.selenium.click_first_xpath("//a[contains(., 'Selenium - Web Browser Automation')]")

        # Clicking on some links for the demo
        self.selenium.alert("Click on link", 2, 2)
        self.selenium.click_first_xpath("//ul[@id='sitemap']//a[contains(., 'Selenium IDE')]")
        self.selenium.alert("Go to download page", 2, 2)
        self.selenium.click_first_xpath("//div[@class='downloadBox']//a")
        self.selenium.page_wait_for_xpath("//h2")
        r = self.selenium.get_element_by_xpath("//a[contains(., 'Mozilla GeckoDriver')]")

        # Running an assert to check if the value is equal to what we expect
        self.l_assertEqual("https://github.com/mozilla/geckodriver/", r.get_attribute("href"))
        self.selenium.alert("End of the browsing test", 2, 2)

    @unittest.skip("This is an example of a skipped test.")
    def test_2_resize_demo(self):
        """
        This test show us a browser resize demo
        :return:
        """
        self.selenium.get('http://www.kissenium.org')
        self.selenium.alert("Here we will show how to resize your browser window", 2, 2)
        self.selenium.resize_window(480, 800)
        self.selenium.alert("480 x 800", 2, 2)
        self.selenium.resize_window(800, 480)
        self.selenium.alert("800 x 480", 2, 2)
        self.selenium.resize_window(1366, 768)
        self.selenium.alert("1366 x 768", 2, 2)
        self.selenium.maximize()
        self.selenium.alert("Maximize the window", 2, 2)

    def test_3_documentation_mode(self):
        """
        This test show us a small "documentation mode" example
        :return:
        """
        self.selenium.get('http://www.adiuvo.fr')
        img = self.selenium.get_element_by_xpath('//div[contains(@class,"l-box-lrg")]//img')
        link = self.selenium.get_element_by_xpath('//a[@href="/blog/tag:SSH"]')
        action = ActionChains(self.selenium.browser)
        action.move_to_element(img).perform()
        action.move_to_element(link)
        action.click()
        action.perform()

        # self.selenium.alert("Here we show the documentation mode.", 20, 2)
        # self.selenium.alert("This mode is experimental, and work only with elements who have id\\'s", 2, 2)
        # self.selenium.scroll_to_xpath("//h2[@id='kissenium--selenium-framework']")
        # self.selenium.dim("kissenium--selenium-framework", 2)
        # self.selenium.alert("Think about scrolling the element before dim the page arround it.", 4, 1)
        # self.selenium.alert("Use \\'self.st.hover_by_xpath\\'", 3, 2)
        # self.selenium.scroll_to_xpath("//h2[@id='functionalities-done-and-to-do']")
        # self.selenium.dim("functionalities-done-and-to-do", 2)
        # self.selenium.scroll_to_xpath("//h2[@id='authors-contributors']")
        # self.selenium.dim("authors-contributors", 2)
