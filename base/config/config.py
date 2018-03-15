# coding: utf-8
"""Kissenium configuration module
"""

import configparser


class Config:
    """Obtain the configuration value or the default fallback value from this class

    :String config_file (optionnal): path of filename
    """

    def __init__(self, config_file='kissenium.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_config(self):
        """Get the configuration object.

        :return::

            Config()
        """
        return self.config

    def get_default(self, parameter, default):
        """Get the config parameter or the default fallback value

        :String parameter: Parameter name
        :String default: Fallback value

        Returns:
            String
        """
        if parameter in self.config['Kissenium']:
            param = self.config['Kissenium'][parameter]
        else:
            param = default
        return param

    def get_run_parallel(self):
        """Get the run parallel config.

        :String return::

            True, False
        """
        return self.get_default('RunParallel', 'False')

    def get_max_parallel(self):
        """Get the max parallel config.

        :String return::

            True, False
        """

        return self.get_default('MaxParallel', 5)

    def get_log_level(self):
        """Get the log level

        :String return::

            DEBUG, INFO, WARNING, ERROR
        """
        return self.get_default('LogLevel', 'DEBUG')

    def get_capture_on_assert_fail(self):
        """Get the capture on assert fail.

        :String return::

            True, False
        """

        return self.get_default('CaptureOnAssertFail', 'True')

    def get_capture_on_fail(self):
        """Get the capture on fail.

        :String return::

            True, False
        """
        return self.get_default('CaptureOnFail', 'True')

    def get_capture_size(self):
        """Get the capture size.

        :String return::

            True, False
        """
        if self.get_run_parallel() == 'True':
            param = 'Browser'
        else:
            param = self.get_default('CaptureSize', 'Browser')
        return param

    def get_fail_on_assert_error(self):
        """Get fail on assert error.

         :String return::

            True, False
         """
        return self.get_default('FailOnAssertError', 'True')

    def get_fail_on_error(self):
        """Get fail on error.

        :String return::

            True, False
        """
        return self.get_default('FailOnError', 'True')

    def get_record_scenarios(self):
        """Get record scenarios

        :String return::

            True, False
        """
        if self.get_run_parallel() == 'True':
            param = 'False'
        else:
            param = self.get_default('RecordScenarios', 'True')
        return param

    def get_capture_end_of_test(self):
        """Get capture end of test.

        :String return::

            True, False
        """

        return self.get_default('CaptureEndOfTest', 'False')

    def get_page_wait(self):
        """Get page wait.

        :Integer return::

            seconds
        """
        return self.get_default('PageWait', 5)

    def get_browser(self):
        """Get browser.

        :String return::

            Firefox, Chrome
        """
        return self.get_default('Browser', "Chrome")

    def get_browser_size(self):
        """Get Browser size.

        :String return::

            width x height
        """
        return self.get_default('BrowserSize', "Maximize")

    def get_message_status(self):
        """Get message status.

        :String return::

            True, False
        """
        return self.get_default('BrowserMessage', False)

    def get_dim_status(self):
        """Get dimentions status

        :String return::

            True, False
        """
        return self.get_default('DimForDemo', False)
