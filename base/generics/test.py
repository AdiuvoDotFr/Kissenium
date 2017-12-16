# coding: utf-8

from base.capture.record import Record
from base.generics import BaseTest


class GenericTest(BaseTest):

    """
        This test take care of the parameters sets in kissenium.ini about recording the whole tests and taking a capture
        at the end of the test. If you want your test to always have a video record, please use the GenericTestVideo
        class instead.
        You also have a GenericTestCapture who will take a screenshot at each end of test.
        Please refer to config.py to learn about the parameters to be set in kissenium.ini
    """

    def setUp(self):
        self.self_setup()
        if self.config.get_record_scenarios() == 'True':
            self.recorder = Record(self.__class__.__name__, self._testMethodName, self.browser)
            self.recorder.start()

    def tearDown(self):
        if self.config.get_capture_end_of_test() == 'True':
            self.take_capture()

        self.self_teardown()

        if self.config.get_record_scenarios() == 'True':
            self.recorder.stop()
