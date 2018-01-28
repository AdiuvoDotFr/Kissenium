# coding: utf-8

"""
Module record: recording the screen where is running all your tests
"""

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
    """
    This class permit to record the local screen where is running the selenium test
    """
    stop_recording = False
    scenario = ""

    def __init__(self, scenario, test):
        """
        Note: if we wan't to record distant execution of kissenium (not implemented for now),
        # we could think of using vnc server on the remote executor
        :param scenario: Scenario name
        :param test: Test name
        """
        threading.Thread.__init__(self)
        self.scenario = scenario
        self.reports_folder = SmallTools.get_reports_folder(self.scenario)
        self.test = test
        self.cancelled = False
        self.config = Config()
        self.logger = Log4Kissenium.get_logger("Kissenium")

    def start(self):
        """
        Start recording your screen
        :return:
        """
        try:
            thread = threading.Thread(name='ScreenRecorder', target=self.record_screen)
            thread.start()
        except Exception as e:
            self.logger.error("Threading exception")
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def record_screen(self):
        """
        Record the screen
        """
        # TODO The mac solution might be the nicest solution for every system
        if Platform.get_os() == "mac":
            self.logger.info("Record video on mac")
            self.ffmpeg_record_mac()
            self.ffmpeg_merge_tmp_videos()
        else:
            self.logger.info("Record video on linux or windows")
            with mss.mss() as sct:
                i = 0
                while not self.stop_recording:
                    thread = threading.Thread(name='ScreenRecorderCapture',
                                              target=self.take_captures(sct, i))
                    thread.start()
                    i += 1
                self.generate_video()
        self.clean_tmp()

    def stop(self):
        """
        Stop the current record action
        :return:
        """
        self.stop_recording = True

    def generate_video(self):
        """
        Generate videos from bunch of images, make the last image
        last longer in the video
        :return:
        """
        try:
            filelist = sorted(glob.glob("reports/tmp/" + self.test + "-*.png"))
            last_image = max(filelist, key=os.path.getctime)
            os.system('ffmpeg -loglevel panic -hide_banner -nostats -framerate 5 -i reports/tmp/'
                      + self.test + '-%06d.png -c:v libx264 -vf "format=yuv420p" reports/tmp/'
                      + self.test + '_body.avi')
            os.system('ffmpeg -loglevel panic -hide_banner -nostats -loop 1 -t 1 -i '
                      + last_image + ' -c:v libx264 -vf "format=yuv420p" reports/tmp/'
                      + self.test + '_lastimg.avi')
            os.system('ffmpeg -loglevel panic -hide_banner -nostats -i "concat:reports/tmp/'
                      + self.test + '_body.avi|reports/tmp/' + self.test + '_lastimg.avi" -c copy '
                      + self.reports_folder + self.test + '.avi')
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def take_captures(self, sct, i):
        """
        Take capture of the screen
        :param sct:
        :param i:
        :return:
        """
        try:
            sct_img = sct.grab(sct.monitors[1])
            img = Image.frombytes('RGBA', sct_img.size, bytes(sct_img.raw), 'raw', 'BGRA')
            img = img.convert('RGB')
            output = 'reports/tmp/' + self.test + '-' + "{0:0=6d}".format(i) + '.png'
            img.save(output)
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def clean_tmp(self):
        """
        Clean the tmp dir after generated the video
        :return:
        """
        try:
            target = glob.glob("reports/tmp/" + self.test + "*")
            SmallTools.delete_from_glob(target)
        # TODO Delete exception
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def ffmpeg_record_mac(self):
        """
        Take many small video of the screen while not self.stop.recording
        :return:
        """
        try:
            i = 0
            while not self.stop_recording:
                command = 'ffmpeg -loglevel panic -hide_banner -nostats -f avfoundation -i "1" ' \
                          '-c:v libx264 -vf "format=yuv420p" -r 25 -t 2 reports/tmp/' \
                          + self.test + '-' + str("{0:0=4d}".format(i)) + '.avi'
                arguments = shlex.split(command)
                subprocess.Popen(arguments)
                time.sleep(2)
                i += 1
        # TODO Subprocess exception
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    def ffmpeg_merge_tmp_videos(self):
        """
        Generate long video from bunch of small videos
        :return:
        """
        try:
            if Platform.get_os() == "mac":
                video_list = ""
                video_list_glob = sorted(glob.glob('reports/tmp/' + self.test + '-*.avi'))
                for video in video_list_glob:
                    start = "" if video_list == "" else "|"
                    video_list += start + video
                self.logger.debug(video_list)
                os.system('ffmpeg -loglevel panic -hide_banner -nostats -i "concat:' + video_list
                          + '" -c copy ' + self.reports_folder + self.test + '.avi')
            else:
                self.logger.error('Not handled for now.')
        # TODO os system exception
        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
