# coding: utf-8

import glob
import os
import traceback

from jinja2 import Environment, FileSystemLoader

from base.logs.log import Log4Kissenium
from base.reports.results_parser import ResultsParser


class HtmlRender:
    title = "Test results"
    filename = "index.html"
    files = []

    def __init__(self, results, start):
        self.tpl_env = Environment(autoescape=False,
                                   loader=FileSystemLoader(os.path.join("resources/", 'html')),
                                   trim_blocks=False)
        self.logger = Log4Kissenium.get_logger("Kissenium")
        self.stats = ResultsParser.get_stats(results, start)
        for file in glob.glob("reports/html/*.html"):
            f = os.path.basename(file)
            if f == "index.html":
                pass
            else:
                self.files.append(f)

    def render_template(self, template_filename, context):
        return self.tpl_env.get_template(template_filename).render(context)

    def create_index(self):
        content = {
            'title': self.title,
            'files': self.files,
            'stats': self.stats
        }
        try:
            with open("reports/html/" + self.filename, 'w') as f:
                index = self.render_template('kissenium-index-template.html', content)
                f.write(index)
        except (OSError, IOError) as e:
            self.logger('Error while creating file')
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
