#!/usr/bin/env python3
# coding: utf-8
import glob
import sys
from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner
from utils.log import Log4Kissenium
from utils.sm_tools import SmallTools
import scenarios


class Runner:

    def __init__(self):
        self.prepare_for_run()
        self.logger = Log4Kissenium().setup("Kissenium", "Kissenium")
        self.logger.info("Logger created.")
        self.test_classes_to_run = [scenarios.TestDemo]
        self.loader = TestLoader()
        self.suites = []

    @staticmethod
    def clean_reports_folder():
        reports_list = glob.glob("reports/*")
        globs = [reports_list]
        for g in globs:
            SmallTools.delete_from_glob(g)

    def prepare_for_run(self):
        self.clean_reports_folder()
        SmallTools.check_path("reports/tmp")

    def run(self):
        for test_class in self.test_classes_to_run:
            suite = self.loader.loadTestsFromTestCase(test_class)
            self.suites.append(suite)

        suite = TestSuite(self.suites)
        test_runner = HTMLTestRunner(output='html', report_title='Kissenium')
        results = test_runner.run(suite)
        self.logger.info("All tests have been executed. Kissenium will stop now.")
        sys.exit(not results.wasSuccessful())
        # xml = dicttoxml(results., custom_root='test', attr_type=False)
        # SmallTools.create_file('Xml', 'Kissenium.xml', xml)


if __name__ == '__main__':
    runner = Runner()
    runner.run()
