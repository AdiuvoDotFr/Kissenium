# coding: utf-8

"""
Read and write data from and to csv file
"""

import csv
from base.tools.sm_tools import SmallTools

class Csv:
    """
    Open a csv and read or write data to it, or create a csv file to write data.
    """

    def __init__(self, file, delimiter=',', quotechar='|'):
        """
        Instanciate csv class. You can manipulate your csv file via this class.
        Don't forget to save (self.save()) if any modification at the end.
        :param file: your file path (relative to kissenium)
        :param delimiter: Csv file delimiter
        """
        self.file = file
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.csv = self.open()

    def open(self):
        with open(self.file, newline='') as file:
            return csv.reader(file, delimiter=self.delimiter, quotechar=self.quotechar)

    def close(self):
        pass

    def read(self):
        pass

    def save(self):
        with open(self.file, 'wb', newline='') as file:
            csv.writer(file)
