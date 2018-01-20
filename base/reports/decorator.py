# coding: utf-8


def exception(message=None):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param logger: The logging object
    @param logger: The message to print on error
    @param logger: The screenshot object, None if no screenshot to take
    """

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                if not message == None:
                    self.logger.error(message)
                self.logger.error('[%s] Error is : %s' %(func.__name__, e))
                if self.config.get_capture_on_fail() == "True":
                    if not 'browser' in dir(self) and not 'screenshot' in dir(self) :
                        self.logger.error('Can\'t take a screenshot, either <browser> or <screenshot> is <None>')
                    else :
                        self.screenshot.capture(self.browser, message)
                if self.config.get_fail_on_error() == "True":
                    raise Exception(message)
                return False
            raise
        return wrapper
    return decorator