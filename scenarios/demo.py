# coding: utf-8
import unittest
import time
from utils.generics.test import GenericTest


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
            from utils.generic_test_capture import GenericTestCapture
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
        r = self.st.get_element_by_xpath(self.browser, "//h1[@class='splash-head']")
        self.assertEqual("DÉVÉLOPPEMENT INFORMATIQUE, ADMINISTRATION SYSTÈMES LINUX ET WINDOWS", r.text)
        self.st.click_first_xpath(self.browser, "//a[contains(., 'Générateur de mots de passe')]")
        challenge = self.st.get_element(self.browser, "ID", "challenge")
        secret = self.st.get_element(self.browser, "ID", "secret")
        challenge.send_keys("1 selenium")
        secret.send_keys("selenium")
        self.st.get_element_by_xpath(self.browser,
                                     "//button[@type='submit' and contains(., 'Lancez le calcul!')]").click()
        r = self.st.get_element_by_xpath(self.browser,
                                         "//textarea[@placeholder = 'Les mots générés apparaîtrons ici.']").get_attribute(
            'value')
        self.l_assertEqual("VET GWEN GOOF TOO MANA CARL (43B2 3A3B 20DB 6EC7)", r)

    def test_3_from_google_search(self):
        """
        Run a test wich start from google
        :return:
        """
        """ Our first assert will be to check the google title """
        self.browser.get('https://www.google.fr')
        self.l_assertIn('Google', self.browser.title, False)

        """ We start by searching for selenium into google """
        search_input = self.st.get_element_by_xpath(self.browser, "//input[@title='Rechercher']")
        search_input.send_keys("selenium")
        self.st.get_element_by_xpath(self.browser, "//input[@value='Recherche Google']").click()

        """ For the demo we will log every page name in the result of google """
        g_results = self.st.get_elements_by_xpath(self.browser, '//div[@id="res"]//h3//a')
        for gr in g_results:
            self.logger.info("Element iteration demo : " + gr.text)

        """ We first go into wikipedia, run an assert, and then go back """
        self.st.click_first_xpath(self.browser, "//a[contains(., 'Sélénium — Wikipédia')]")
        title = self.st.get_element_by_id(self.browser, 'firstHeading')
        self.l_assertIn("Sélénium", title.text)
        self.browser.back()

        """ We are going to the selenium official website """
        self.st.click_first_xpath(self.browser, "//a[contains(., 'Selenium - Web Browser Automation')]")

        """ Clicking on some links for the demo """
        self.st.click_first_xpath(self.browser, "//ul[@id='sitemap']//a[contains(., 'Selenium IDE')]")
        self.st.click_first_xpath(self.browser, "//div[@class='downloadBox']//a")
        self.st.page_wait_for_xpath(self.browser, "//h2")
        r = self.st.get_element_by_xpath(self.browser, "//a[contains(., 'Mozilla GeckoDriver')]")

        """ Running an assert to check if the value is equal to what we expect """
        self.l_assertEqual("https://github.com/mozilla/geckodriver/", r.get_attribute("href"))

    def test_4_assert_log(self):
        """
        This a example of log assert method.
        This test will fail
        In this you will see how you can manage your asserts to continue to run (or not) with some simple parameters.
        The parameter passed to the l_assert function (True|False) will always override the
        Config['Kissenium']['FailOnAssertError'] parameter.
        :return:
        """
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
