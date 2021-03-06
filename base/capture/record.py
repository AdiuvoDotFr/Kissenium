# coding: utf-8

import glob
import os
import shlex
import subprocess
import threading
import time
import traceback

import mss
from PIL import Image

from base.config.config import Config
from base.logs.log import Log4Kissenium
from base.tools.platform import Platform
from base.tools.sm_tools import SmallTools


class Record(threading.Thread):
    stop_recording = False
    scenario = ""

    def __init__(self, scenario, test):
        # Note: if we wan't to record distant execution of kissenium (not implemented for now), we could think of using
        # vnc server on the remote executor
        threading.Thread.__init__(self)
        self.scenario = scenario
        self.reports_folder = SmallTools.get_reports_folder(self.scenario)
        self.test = test
        self.cancelled = False
        self.config = Config()
        self.logger = Log4Kissenium.get_logger("Kissenium")

    def start(self):
        try:
            t = threading.Thread(name='ScreenRecorder', target=self.record_screen)
            t.start()
        except Exception as e:
            self.logger.error("Threading exception")
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def record_screen(self):
        # The mac solution might be the nicest solution for every system
        # To be more tested
        if Platform.get_os() == "mac":
            self.logger.info("Record video on mac")
            self.ffmpeg_record_mac()
            self.ffmpeg_merge_tmp_videos()
        else:
            self.logger.info("Record video on linux or windows")
            with mss.mss() as sct:
                i = 0
                while not self.stop_recording:
                    th = threading.Thread(name='ScreenRecorderCapture', target=self.take_captures(sct, i))
                    th.start()
                    i += 1
                self.generate_video()
        self.clean_tmp()

    def stop(self):
        self.stop_recording = True

    def generate_video(self):
        try:
            filelist = sorted(glob.glob("reports/tmp/" + self.test + "-*.png"))
            last_image = max(filelist, key=os.path.getctime)
            os.system('ffmpeg -loglevel panic -hide_banner -nostats -f image2 -framerate 8 -i reports/tmp/' + self.test
                      + '-%06d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p reports/tmp/' + self.test + '_body.avi')
            os.system('ffmpeg -loglevel panic -hide_banner -nostats -loop 1 -t 1 -i ' + last_image
                      + ' -c:v libx264 -vf "format=yuv420p" reports/tmp/' + self.test + '_lastimg.mp4')
            os.system('ffmpeg -loglevel panic -hide_banner -nostats -i "concat:reports/tmp/' + self.test
                      + '_body.mp4|reports/tmp/' + self.test + '_lastimg.mp4" -c copy ' + self.reports_folder
                      + self.test + '.mp4')
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def take_captures(self, sct, i):
        try:
            sct.shot(output='reports/tmp/' + self.test + '-' + "{0:0=6d}".format(i) + '.png')
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def clean_tmp(self):
        try:
            g = glob.glob("reports/tmp/" + self.test + "*")
            SmallTools.delete_from_glob(g)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def ffmpeg_record_mac(self):
        try:
            i = 0
            while not self.stop_recording:
                command = 'ffmpeg -loglevel panic -hide_banner -nostats -f avfoundation -i "1" -c:v libx264 -vf '\
                          + '"format=yuv420p" -r 25 -t 2 reports/tmp/' \
                          + self.test + '-' + str("{0:0=4d}".format(i)) + '.avi'
                arguments = shlex.split(command)
                subprocess.Popen(arguments)
                time.sleep(2)
                i += 1
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def ffmpeg_merge_tmp_videos(self):
        try:
            if Platform.get_os() == "mac":
                vl = ""
                videolist = sorted(glob.glob('reports/tmp/' + self.test + '-*.avi'))
                for video in videolist:
                    s = "" if vl == "" else "|"
                    vl += s + video
                self.logger.debug(vl)
                os.system('ffmpeg -loglevel panic -hide_banner -nostats -i "concat:' + vl + '" -c copy '
                          + self.reports_folder + self.test + '.avi')
            else:
                self.logger.error('Not handled for now.')
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
