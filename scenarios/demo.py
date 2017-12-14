# coding: utf-8
import unittest
import time
from base.generics.test import GenericTest


class TestDemo(GenericTest):

    """
        This is a demo class who will show-up most of the functionalities of this small test environment.
        Here you will learn how to :
            * record a video or a capture of the end of your test
            * run a test on a quite simple example (make a request on google, clic to visit a website, submit a form, ...)
            * how to log some importants things about your tests (keep in mind that you will need to understand whats was
                going wrong when it fails)
        ---
        If you want to take a capture instead of the video, change the import to
            from base.generic_test_capture import GenericTestCapture
        and the extend of the class to
            class SeleniumPoc(GenericTestCapture):
        ---
        If you need to run your tests in a specific order, you can add an order number after the method keyword 'test'
        Like this:
            def test_4_test_name(self):
                # My test
    """

    @unittest.skip("This is an example of a skipped test.")
    def test_1_skip(self):
        """ This test is skipped """

    def test_2_adiuvo_otp(self):
        """
        Run a test on a website, and do an assert on a OTP page
        :return:
        """
        self.browser.get('https://www.adiuvo.fr')
        self.js.message(self.browser, "Here is a simple test demo in a website.", 4, 4)
        r = self.st.get_element_by_xpath(self.browser, "//h1[@class='splash-head']")
        self.assertEqual("DÉVÉLOPPEMENT INFORMATIQUE, ADMINISTRATION SYSTÈMES LINUX ET WINDOWS", r.text)
        self.js.message(self.browser, "Page title has been tested", 2, 2)
        self.st.click_first_xpath(self.browser, "//a[contains(., 'Générateur de mots de passe')]")

        """ Testing the OTP form """
        self.js.message(self.browser, "Testing the OTP form", 10, 1)
        """ Scroll to the form """
        self.st.hover_by_xpath(self.browser, "//form[@id='otp_form']")

        """ Fill the form """
        challenge = self.st.get_element(self.browser, "ID", "challenge")
        secret = self.st.get_element(self.browser, "ID", "secret")
        self.js.message(self.browser, "Sending challenge input", 2, 2)
        challenge.send_keys("1 selenium")
        self.js.message(self.browser, "Sending secret input", 2, 2)
        secret.send_keys("selenium")

        """ Click on generate """
        self.js.message(self.browser, "Click to generate", 2, 2)
        self.st.get_element_by_xpath(self.browser,
                                     "//button[@type='submit' and contains(., 'Lancez le calcul!')]").click()
        r = self.st.get_element_by_xpath(self.browser,
                                         "//textarea[@placeholder = 'Les mots générés apparaîtrons ici.']")\
                                         .get_attribute('value')
        self.l_assertEqual("VET GWEN GOOF TOO MANA CARL (43B2 3A3B 20DB 6EC7)", r)
        self.js.message(self.browser, "Assert is ok", 2, 1)

    def test_3_from_google_search(self):
        """
        Run a test wich start from google
        :return:
        """
        """ Our first assert will be to check the google title """
        self.browser.get('https://www.google.fr')
        self.js.message(self.browser, "This test will go trough standard browsing on the web with some tests.", 5, 3)
        self.l_assertIn('Google', self.browser.title, False)

        """ We start by searching for selenium into google """
        search_input = self.st.get_element_by_xpath(self.browser, "//input[@title='Rechercher']")
        self.js.message(self.browser, "We are starting by searching for selenium in google", 2, 1)
        search_input.send_keys("selenium")
        self.st.get_element_by_xpath(self.browser, "//input[@value='Recherche Google']").click()

        """ For the demo we will log every page name in the result of google """
        g_results = self.st.get_elements_by_xpath(self.browser, '//div[@id="res"]//h3//a')
        for gr in g_results:
            self.logger.info("Element iteration demo : " + gr.text)

        """ We first go into wikipedia, run an assert, and then go back """
        self.st.click_first_xpath(self.browser, "//a[contains(., 'Wikipédia')]")
        self.js.message(self.browser, "Browsing wikipedia page", 2, 1)
        self.js.message(self.browser, "Testing the page title", 2, 1)
        title = self.st.get_element_by_id(self.browser, 'firstHeading')
        self.l_assertIn("Selenium", title.text)
        self.js.message(self.browser, "Page title is ok!", 2, 1)
        self.js.message(self.browser, "Go to the previous page (self.browser.page)", 1, 1)
        self.browser.back()

        """ We are going to the selenium official website """
        self.js.message(self.browser, "Go to the selenium website", 2, 2)
        self.st.click_first_xpath(self.browser, "//a[contains(., 'Selenium - Web Browser Automation')]")

        """ Clicking on some links for the demo """
        self.js.message(self.browser, "Click on link", 2, 2)
        self.st.click_first_xpath(self.browser, "//ul[@id='sitemap']//a[contains(., 'Selenium IDE')]")
        self.js.message(self.browser, "Go to download page", 2, 2)
        self.st.click_first_xpath(self.browser, "//div[@class='downloadBox']//a")
        self.st.page_wait_for_xpath(self.browser, "//h2")
        r = self.st.get_element_by_xpath(self.browser, "//a[contains(., 'Mozilla GeckoDriver')]")

        """ Running an assert to check if the value is equal to what we expect """
        self.l_assertEqual("https://github.com/mozilla/geckodriver/", r.get_attribute("href"))
        self.js.message(self.browser, "End of the browsing test", 2, 2)

    def test_4_resize_demo(self):
        """
        This test show us a browser resize demo
        :return:
        """
        self.browser.get('http://www.kissenium.org')
        self.js.message(self.browser, "Here we will show how to resize your browser window", 2, 2)
        self.resize_window(480, 800)
        self.js.message(self.browser, "480 x 800", 2, 2)
        self.resize_window(800, 480)
        self.js.message(self.browser, "800 x 480", 2, 2)
        self.resize_window(1366, 768)
        self.js.message(self.browser, "1366 x 768", 2, 2)
        self.maximize()
        self.js.message(self.browser, "Maximize the window", 2, 2)

    def test_5_documentation_mode(self):
        """
        This test show us a small "documentation mode" example
        :return:
        """
        self.browser.get('http://www.kissenium.org')
        self.js.message(self.browser, "Here we show the documentation mode.", 20, 2)
        self.js.message(self.browser, "This mode is experimental, and work only with elements who have id\\'s", 2, 2)
        self.st.hover_by_xpath(self.browser, "//h2[@id='kissenium--selenium-framework']")
        self.js.dim_by_id(self.browser, "kissenium--selenium-framework", 2)
        self.js.message(self.browser, "Think about scrolling the element before dim the page arround it.", 4, 1)
        self.js.message(self.browser, "Use \\'self.st.hover_by_xpath\\'", 3, 2)
        self.st.hover_by_xpath(self.browser, "//h2[@id='functionalities-done-and-to-do']")
        self.js.dim_by_id(self.browser, "functionalities-done-and-to-do", 2)
        self.st.hover_by_xpath(self.browser, "//h2[@id='authors-contributors']")
        self.js.dim_by_id(self.browser, "authors-contributors", 2)

    def test_6_assert_log(self):
        """
        This a example of log assert method.
        This test will fail
        In this you will see how you can manage your asserts to continue to run (or not) with some simple parameters.
        The parameter passed to the l_assert function (True|False) will always override the
        Config['Kissenium']['FailOnAssertError'] parameter.
        :return:
        """
        self.browser.get('http://www.kissenium.org')
        self.js.message(self.browser, "There are just asserts examples working in the background.", 30, 1)
        self.js.message(self.browser, "You can change the parameter FailOnAssertError to see what\\'s going on.", 30, 1)
        self.l_assertEqual(1, 1, False)
        self.l_assertEqual(1, 2, False)
        self.l_assertNotEqual(1, 2, False)
        self.l_assertNotEqual(1, 1, False)
        self.l_assertFalse(False, False)
        self.l_assertFalse(True, False)
        self.l_assertTrue(True, False)
        self.l_assertTrue(False, False)
        self.l_assertIn("e", "test", False)
        self.l_assertIn("a", "test", False)
        self.l_assertNotIn("a", "test", False)
        self.l_assertNotIn("e", "test", False)
        self.l_assertIsNone(None, False)
        self.l_assertIsNone("test")
        # Thoses assert will never be run
        self.l_assertIsNotNone("test", False)
        self.l_assertIsNotNone(None, False)
