# coding: utf-8

import datetime
import traceback

from base.logs.log import Log4Kissenium


class ResultsParser:

    @staticmethod
    def get_stats(results, start):
        logger = Log4Kissenium.get_logger("Kissenium")
        try:
            duration = datetime.datetime.now() - start
            stats = {
                'tests_runned': results.testsRun,
                'skipped' : len(results.skipped),
                'failures' : len(results.failures),
                'successes': len(results.successes),
                'errors': len(results.errors),
                'duration': str(datetime.timedelta(seconds=duration.seconds)),
            }
            return stats
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    @staticmethod
    def add_test_in(r, t, status):
        try:
            if (status == "success"):
                obj = t
                mes = None
            else:
                obj = t[0]
                mes = t[1]
            tn = obj.test_name
            ti = obj.test_id.split('.')[-1]

            if not tn in r:
                r[tn] = {}

            if not ti in r[tn]:
                r[tn][ti] = {}
            else:
                raise ValueError('Test already in array. Raising error')

            r[tn][ti]['object'] = obj
            r[tn][ti]['message'] = mes
            r[tn][ti]['status'] = status
        except ValueError as e:
            logger = Log4Kissenium.get_logger("Kissenium")
            logger.error(e)
            logger.error(traceback.format_exc())
        except Exception as e:
            logger = Log4Kissenium.get_logger("Kissenium")
            logger.error(e)
            logger.error(traceback.format_exc())

    @staticmethod
    def results_to_array(results):
        r = {}
        # Successes
        for t in results.successes:
            ResultsParser.add_test_in(r, t, "success")
        # Errors
        for t in results.errors:
            ResultsParser.add_test_in(r, t, "error")
        # Failures
        for t in results.failures:
            ResultsParser.add_test_in(r, t, "failure")
        # Skipped
        for t in results.skipped:
            ResultsParser.add_test_in(r, t, "skipped")
        return r