# coding: utf-8
import mss
from utils.sm_tools import SmallTools
from utils.config import Config
from PIL import Image


class ScreenCapture:
    scenario = ""

    def __init__(self, scenario, test):
        self.scenario = scenario
        self.test = test
        self.cancelled = False
        self.config = Config()
        self.reports_folder = SmallTools.get_reports_folder(self.scenario)

    def capture(self, browser, suffix=''):
        if suffix != '':
            suffix = '-' + suffix
        filename = SmallTools.sanitize_filename(self.test + suffix + '.png')

        if self.config.get_capture_size() == 'Full':
            self.capture_screen(filename)
        else:
            self.capture_browser(browser, filename)

    def capture_screen(self, filename):
        with mss.mss() as sct:
            sct_img = sct.grab(sct.monitors[1])
            img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
            img = img.convert('RGB')
            output = self.reports_folder + filename
            img.save(output)

    def capture_browser(self, browser, filename):
        reports_folder = SmallTools.get_reports_folder(self.scenario)
        browser.get_screenshot_as_file(reports_folder + filename)
