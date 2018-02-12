# coding: utf-8

import traceback
import xml.etree.cElementTree as ET
from xml.dom import minidom

from base.logs.log import Log4Kissenium
from base.reports.results_parser import ResultsParser
from base.tools.sm_tools import SmallTools


class JunitResults:

    def __init__(self, results, start):
        self.stats = ResultsParser.get_stats(results, start)
        self.results = ResultsParser.results_to_array(results)

    def generate(self):
        """Generate

        :returns: Nothing

        """
        logger = Log4Kissenium.get_logger("Kissenium")
        try:
            root = ET.Element("testsuites")
            #root.set('duration', self.stats['duration'])

            for k, v in self.results.items():
                test, successes, errors, failures, skipped = (0,)*5
                # Create the testsuite element, this will be completed after the testcases iteration
                xml_ts = ET.SubElement(root, "testsuite")

                # Iterate over testcases
                for ki, vi in v.items():
                    test += 1
                    if vi['status'] == 'success':
                        successes += 1
                    elif vi['status'] == 'error':
                        errors += 1
                    elif vi['status'] == 'failure':
                        failures += 1
                    elif vi['status'] == 'skipped':
                        skipped += 1

                    xml_tc = ET.SubElement(xml_ts, "testcase", classname=k.replace('.', '/'),
                                           name=k)
                    if not vi['status'] == "success":
                        ET.SubElement(xml_tc, vi['status']).text = vi['message']

                xml_ts.set('errors', str(errors))
                xml_ts.set('failures', str(failures))
                xml_ts.set('skipped', str(skipped))
                xml_ts.set('tests', str(test))
                xml_ts.set('name', k.split('.')[-1])
                xml_ts.set('package', k.replace('.', '/'))

            s = minidom.parseString(ET.tostring(root, 'utf-8'))
            SmallTools.create_file('Kissenium/', 'reports.xml', s.toprettyxml(indent="  "))

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
