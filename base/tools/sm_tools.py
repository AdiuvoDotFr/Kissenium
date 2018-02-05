# coding: utf-8

import os
import re
import shutil
import traceback
import logging


class SmallTools:

    @staticmethod
    def check_path(path):
        """
        Check if folder exist or not. If it doesn't exist, this method create it

        :param path: path of your folder
        :return: Nothing
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def get_reports_folder(path):
        """This method return the relative ath of your reports folder. Just give it the report your
        want to make.

        :param path: Pathof your report folder
        :return: Relative path of your report folder
        """
        if path.startswith('/'):
            path = path.replace('/', '', 1)
        if not path.endswith('/'):
            path += '/'

        final_path = "reports/" + path

        SmallTools.check_path(final_path)
        return final_path

    @staticmethod
    def delete_from_glob(g):
        """Delete all folders and files givenin a glob

        :param g: Glob
        :return: Nothing
        """
        try:
            for f in g:
                if os.path.isdir(f):
                    shutil.rmtree(f)
                else:
                    os.remove(f)
        except (OSError, IOError) as e:
            logger = logging.getLogger("Kissenium")
            logger.error(e)
            logger.error(traceback.format_exc())

    @staticmethod
    def create_file(path, file, content):
        """Create a file with a specified content

        :param path: The path of your file. This path will be integrated in the results folder
        :param file: The name of your file
        :param content: The content of your file
        :return: Nothing
        """
        path = SmallTools.get_reports_folder(path)
        file_path = path + file
        with open(file_path, 'w') as f:
            for l in content:
                f.write(l)

    @staticmethod
    def sanitize_filename(filename):
        return re.sub('[^A-Za-z0-9.]+', '_', filename)

    @staticmethod
    def get_lines_from_file(path, filename):
        with open(path + filename, 'r') as f:
            lines = f.readlines()
            f.close()
        return lines
