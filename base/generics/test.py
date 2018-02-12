# coding: utf-8

"""
This class is not used anymore
"""


from base.capture.record import Record
from base.generics.base import BaseTest


class GenericTest(BaseTest):
    """
    This class is not used anymore
    """
    # TODO Check if we need to keep this class or not

    def setUp(self):
        """This is the setup function, it will be call before every test to run

        :return: Nothing

        """
        self.self_setup()
        if self.config.get_record_scenarios() == 'True':
            self.recorder = Record(self.__class__.__name__, self._testMethodName)
            self.recorder.start()

    def tearDown(self):
        """This is the teardown function, it will be call after every test to run

        :return: Nothing

        """
        if self.config.get_capture_end_of_test() == 'True':
            self.take_capture()

        self.self_teardown()

        if self.config.get_record_scenarios() == 'True':
            self.recorder.stop()
