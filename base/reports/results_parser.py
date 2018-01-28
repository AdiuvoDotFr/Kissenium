# coding: utf-8

import datetime
import traceback

from base.logs.log import Log4Kissenium


class ResultsParser:

    @staticmethod
    def get_stats(results, start):
        try:
            duration = datetime.datetime.now() - start
            tests_runned = 0
            skipped = 0
            failures = 0
            successes = 0
            errors = 0

            for key, future in results.items():
                if key == 'single_runner':
                    result = future
                else:
                    result = future.result()

                tests_runned += result.testsRun
                skipped += len(result.skipped)
                failures += len(result.failures)
                successes += len(result.successes)
                errors += len(result.errors)

            stats = {
                'tests_runned': tests_runned,
                'skipped' : skipped,
                'failures' : failures,
                'successes': successes,
                'errors': errors,
                'duration': str(datetime.timedelta(seconds=duration.seconds)),
            }
            return stats
        except Exception as e:
            logger = Log4Kissenium.get_logger("Kissenium")
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

        for key, future in results.items():
            if key == 'single_runner':
                result = future
            else:
                result = future.result()

            for t in result.successes:
                ResultsParser.add_test_in(r, t, "success")
            # Errors
            for t in result.errors:
                ResultsParser.add_test_in(r, t, "error")
            # Failures
            for t in result.failures:
                ResultsParser.add_test_in(r, t, "failure")
            # Skipped
            for t in result.skipped:
                ResultsParser.add_test_in(r, t, "skipped")
        return r