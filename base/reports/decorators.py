# coding: utf-8


def exception(message=None):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur

    @param message: The message to print
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


def assertion_error():
    """
    A decorator to use in comparing assert

    @param operator: The operator used for the assert
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                message = '[%s] Error is : %s' % (func.__name__, e)
                self.logger.error(message)
                self.has_error = True
                self.take_assert_capture(suffix=message)

                if args[-1] is True:
                    raise AssertionError(message)
                elif args[-1] is not None and args[-1] is False:
                    return
                elif not self.config.get_fail_on_assert_error() == 'False':
                    raise AssertionError(message)
        return wrapper
    return decorator