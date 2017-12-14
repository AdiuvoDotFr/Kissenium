import traceback
import datetime
from base.log import Log4Kissenium

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