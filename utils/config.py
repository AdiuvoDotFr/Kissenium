import configparser


class Config:

    def __init__(self):
        self.config = None
        self.generate_configuration()

    def generate_configuration(self):
        self.config = configparser.ConfigParser()
        self.config.read('kissenium.ini')

    def get_config(self):
        return self.config

    def get_default(self, parameter, default):
        if parameter in self.config['Kissenium']:
            return self.config['Kissenium'][parameter]
        else:
            return default

    def get_log_level(self):
        return self.get_default('LogLevel', 'DEBUG')

    def get_capture_on_assert_fail(self):
        return self.get_default('CaptureOnAssertFail', 'True')

    def get_capture_on_fail(self):
        return self.get_default('CaptureOnFail', 'True')

    def get_capture_size(self):
        return self.get_default('CaptureSize', 'Browser')

    def get_fail_on_assert_error(self):
        return self.get_default('FailOnAssertError', 'True')

    def get_fail_on_error(self):
        return self.get_default('FailOnError', 'True')

    def get_record_scenarios(self):
        return self.get_default('RecordScenarios', 'True')

    def get_capture_end_of_test(self):
        return self.get_default('CaptureEndOfTest', 'False')

    def get_page_wait(self):
        return self.get_default('PageWait', 5)

    def get_browser(self):
        return self.get_default('Browser', "Chrome")
