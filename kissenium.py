#!/usr/bin/env python3
# coding: utf-8

"""Copyright 2017-2018 Adiuvo

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

import datetime
import glob
import sys
from unittest import TestLoader, TestSuite
from concurrent.futures import ThreadPoolExecutor

from HtmlTestRunner import HTMLTestRunner

import scenarios
from base.logs.log import Log4Kissenium
from base.config.config import Config
from base.reports.html import HtmlRender
from base.reports.junit import JunitResults
from base.tools.sm_tools import SmallTools


class Kissenium:
    """Kissenium is a free software to run selenium tests

    To define new scenarios, please check the examples given in ``./scenarios`` folder.

    First run:
        You will need to create a new class file and add it to ``__init__.py``. Then,
        you can declare your new scenario like the following::

            def __init__(self):
                ...
                self.test_classes_to_run = [scenarios.TestDemo, scenarios.ParallelDemo]
                ...

    Then you can run your tests:

        From your virtual environment::

            $(Kissenium) ./kissenium.py

    Note:
        Don't forget to check the `kissenium.ini`` file. Here you will be able to activate
        or deactivate the main functionalities.

    Developers:
        Here are the commands that you will need:
            * Pylint::

                $(Kissenium) pylint kissenium.py base/

            * Documentation::

                $(Kissenium) make clean && make html
    """

    def __init__(self):
        """Init Kissenium Runner class
        """
        self.start = datetime.datetime.now()
        self.prepare_for_run()
        self.config = Config()
        self.logger = Log4Kissenium().setup("Kissenium", "Kissenium")
        self.logger.info("Logger created.")
        self.test_classes_to_run = [scenarios.TestDemo, scenarios.ParallelDemo]
        self.loader = TestLoader()
        self.suites = []

    @staticmethod
    def clean_reports_folder():
        """Clean reports folder on every run

        :return:
        """
        reports_list = glob.glob("reports/*")
        globs = [reports_list]
        for g in globs:
            SmallTools.delete_from_glob(g)

    def prepare_for_run(self):
        """Prepare the report folders for Kissenium execution

        :return:
        """
        self.clean_reports_folder()
        SmallTools.check_path("reports/tmp")

    def execution(self):
        """Execute Kissenium with a single test runner

        :return:
        """
        results = {}
        for test_class in self.test_classes_to_run:
            suite = self.loader.loadTestsFromTestCase(test_class)
            self.suites.append(suite)

        suite = TestSuite(self.suites)
        test_runner = HTMLTestRunner(output='html',
                                     template='resources/html/kissenium-template.html',
                                     report_title='Test report')
        results['single_runner'] = test_runner.run(suite)
        return (results['single_runner'].wasSuccessful()), results

    def parallel_execution(self):
        """Execute kissenium with parallels tests runners

        You can disable (or enable) the parallels runners, and modify the max number of threads in
        ``kissenium.ini``::

            RunParallel = True
            MaxParallel = 5

        Solution for parrallel execution finded here:
            https://stackoverflow.com/questions/38189461/how-can-i-execute-in-parallel-selenium-python-tests-with-unittest

        :return:
        """
        suite = TestSuite()
        results = {}

        for test in self.test_classes_to_run:
            suite.addTest(TestLoader().loadTestsFromTestCase(test))

        with ThreadPoolExecutor(max_workers=int(self.config.get_max_parallel())) as executor:
            list_of_suites = list(suite)
            for test in list_of_suites:
                results[str(test)] = executor.submit(
                    HTMLTestRunner(output='html',
                                   template='resources/html/kissenium-template.html',
                                   report_title=str(test)).run, test)
            executor.shutdown(wait=True)

        for key, future in results.items():
            result = future.result()
            self.logger.debug('[%s] Result is : %s', key, result.wasSuccessful())
            if not result.wasSuccessful():
                return False, results
        return True, results

    def run(self):
        """Run Kissenium tests

        :return:
        """
        self.logger.info('Launching tests ...')
        if self.config.get_run_parallel() == 'True':
            self.logger.info("Test are parallel")
            status, results = self.parallel_execution()
        else:
            self.logger.info("Test are not parallel")
            status, results = self.execution()

        self.logger.info("All tests have been executed. Kissenium will stop now.")
        HtmlRender(results, self.start).create_index()
        JunitResults(results, self.start).generate()
        sys.exit(not status)


if __name__ == '__main__':
    Kissenium().run()
