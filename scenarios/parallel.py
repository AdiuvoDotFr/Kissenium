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

import unittest
import time
from base.generics.test import GenericTest


class ParallelDemo(GenericTest):

    """
        This is a demo class who will show-up most of the functionalities of this small test environment.
        PLease check the kissenium.ini file for more configuration
        If you need to run your tests in a specific order, you can add an order number after the method keyword 'test'
        Like this:
            def test_4_test_name(self):
                # My test
    """

    def test_1_adiuvo_otp(self):
        """
        Run a test on a website, and do an assert on a OTP page
        :return:
        """
        self.selenium.get('https://www.adiuvo.fr')
        self.selenium.alert("Here is a simple test demo in a website.", 4, 4)
        r = self.selenium.get_element_by_xpath("//h1[@class='splash-head']")
        self.l_assertEqual("DÉVÉLOPPEMENT INFORMATIQUE, ADMINISTRATION SYSTÈMES LINUX ET WINDOWS", r.text)
        self.selenium.alert("Page title has been tested", 2, 2)
        self.selenium.click_first_xpath("//a[contains(., 'Générateur de mots de passe')]")

        # Testing the OTP form
        self.selenium.alert("Testing the OTP form", 10, 1)
        # Scroll to the form
        self.selenium.scroll_to_xpath("//form[@id='otp_form']")

        # Fill the form
        self.selenium.alert("Sending challenge input", 2, 2)
        self.selenium.send_keys_by_id("challenge", "1 selenium")
        self.selenium.alert("Sending secret input", 2, 2)
        self.selenium.send_keys_by_id("secret", "selenium")

        # Click on generate
        self.selenium.alert("Click to generate", 2, 2)
        self.selenium.get_element_by_xpath("//button[@type='submit' and contains(., 'Lancez le calcul!')]").click()
        r = self.selenium.get_element_by_xpath("//textarea[@placeholder = 'Les mots générés apparaîtrons ici.']")\
                                         .get_attribute('value')
        self.l_assertEqual("VET GWEN GOOF TOO MANA CARL (43B2 3A3B 20DB 6EC7)", r)
        self.selenium.alert("Assert is ok", 2, 1)

    @unittest.skip("This is an example of a skipped test.")
    def test_2_skip(self):
        """ This test is skipped """

    def test_3_assert_log(self):
        """
        This a example of log assert method.
        This test will fail
        In this you will see how you can manage your asserts to continue to run (or not) with some simple parameters.
        The parameter passed to the l_assert function (True|False) will always override the
        Config['Kissenium']['FailOnAssertError'] parameter.
        :return:
        """
        self.selenium.get('http://www.kissenium.org')
        self.selenium.alert("There are just asserts examples working in the background.", 30, 1)
        self.selenium.alert("You can change the parameter FailOnAssertError to see what\\'s going on.", 30, 1)
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
