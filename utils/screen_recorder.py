# coding: utf-8
import mss
import os
import time
import glob
import threading
from PIL import Image
from utils.sm_tools import SmallTools
from utils.config import Config
from utils.log import Log4Kissenium


class ScreenRecorder(threading.Thread):
    stop_recording = False
    scenario = ""

    def __init__(self, scenario, test, browser):
        threading.Thread.__init__(self)
        self.scenario = scenario
        self.test = test
        self.browser = browser
        self.cancelled = False
        self.config = Config()
        self.logger = Log4Kissenium.get_logger("Kissenium")

    def start(self):
        t = threading.Thread(name='ScreenRecorder', target=self.record_screen)
        t.start()

    def record_screen(self):
        with mss.mss() as sct:
            i = 0
            while not self.stop_recording:
                th = threading.Thread(name='ScreenRecorderCapture', target=self.take_captures(sct, i))
                th.start()
                i += 1

    """
    Not working, Errno11 connction refused
    def record_browser(self):
        # current_time = time.time
        # start = current_time()
        # period = 1 / 12
        i = 0
        self.logger.info("Before while")
        while not self.stop_recording:
            try:
                # self.logger.info("Before if statement %s" % (current_time() - start))
                # if (current_time() - start) > period:
                filename = 'reports/tmp/%s-%s.png' % (self.test, "{0:0=6d}".format(i))
                self.logger.info(filename)
                self.browser.get_screenshot_as_file(filename)
                self.logger.info("Capture taken")
                # start += period
                i += 1
            except Exception as e:
                self.logger.error("Recording browser error : %s" % e)"""

    def stop(self):
        self.stop_recording = True

    def generate_video(self):
        reports_folder = SmallTools.get_reports_folder(self.scenario)
        filelist = glob.glob("reports/tmp/" + self.test + "-*.png")
        last_image = max(filelist, key=os.path.getctime)
        os.system('ffmpeg -loglevel panic -hide_banner -nostats -framerate 5 -i reports/tmp/' + self.test + '-%06d.png -c:v libx264 -vf "format=yuv420p" reports/tmp/' + self.test + '_body.avi')
        os.system('ffmpeg -loglevel panic -hide_banner -nostats -loop 1 -t 1 -i ' + last_image + ' -c:v libx264 -vf "format=yuv420p" reports/tmp/' + self.test + '_lastimg.avi')
        os.system('ffmpeg -loglevel panic -hide_banner -nostats -i "concat:reports/tmp/' + self.test + '_body.avi|reports/tmp/' + self.test + '_lastimg.avi" -c copy ' + reports_folder + self.test + '.avi')

    def take_captures(self, sct, i):
        sct_img = sct.grab(sct.monitors[1])
        img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
        img = img.convert('RGB')
        output = 'reports/tmp/' + self.test + '-' + "{0:0=6d}".format(i) + '.png'
        img.save(output)

    def clean_captures(self):
        g = glob.glob("reports/tmp/" + self.test + "*")
        SmallTools.delete_from_glob(g)
