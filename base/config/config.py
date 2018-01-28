# coding: utf-8

"""
Manipulation of the Kissenium configuration (eg: kissenium.ini)
"""

import configparser


class Config:
    """
    Obtain the configuration value or the default fallback value
    from this class
    """

    def __init__(self, config_file='kissenium.ini'):
        """
        Init the class (you can specify the file if you need
        :param config_file:
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_config(self):
        """
        Get the configuration object
        :return:
        """
        return self.config

    def get_default(self, parameter, default):
        """
        Get the config parameter or the default fallback value
        :param parameter: Parameter name
        :param default: Fallback value
        :return:
        """
        if parameter in self.config['Kissenium']:
            return self.config['Kissenium'][parameter]
        else:
            return default

    def get_run_parallel(self):
        return self.get_default('RunParallel', 'False')

    def get_max_parallel(self):
        return self.get_default('MaxParallel', 5)

    def get_log_level(self):
        """

        :return:
        """
        return self.get_default('LogLevel', 'DEBUG')

    def get_capture_on_assert_fail(self):
        return self.get_default('CaptureOnAssertFail', 'True')

    def get_capture_on_fail(self):
        return self.get_default('CaptureOnFail', 'True')

    def get_capture_size(self):
        if self.get_run_parallel() == 'True':
            return 'Browser'
        else:
            return self.get_default('CaptureSize', 'Browser')

    def get_fail_on_assert_error(self):
        return self.get_default('FailOnAssertError', 'True')

    def get_fail_on_error(self):
        return self.get_default('FailOnError', 'True')

    def get_record_scenarios(self):
        if self.get_run_parallel() == 'True':
            return 'False'
        else:
            return self.get_default('RecordScenarios', 'True')

    def get_capture_end_of_test(self):
        return self.get_default('CaptureEndOfTest', 'False')

    def get_page_wait(self):
        return self.get_default('PageWait', 5)

    def get_browser(self):
        return self.get_default('Browser', "Chrome")

    def get_browser_size(self):
        return self.get_default('BrowserSize', "Maximize")

    def get_message_status(self):
        return self.get_default('BrowserMessage', False)

    def get_dim_status(self):
        return self.get_default('DimForDemo', False)
