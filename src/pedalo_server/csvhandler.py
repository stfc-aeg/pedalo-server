"""Csvfilehandler - a class to write to csv files

This module is used to write a part of data to csv file
which can be used latter for detailed data analysis
"""

import csv

class Csvfilehandler():
    """Class to handle csv file
    """
    def __init__(self,filename,sensor) -> None:
        """Init method to specify file name and sensor that is used

        Args:
            filename (string): a name of the file to write
            sensor (sensor): sensor that is used
        """
        self.filename = filename
        self.sensor = sensor

    def writetofile(self):
        """Write data to file

        This method is used to open file and write data from sensor to the file
        """
        with open (self.filename, 'a') as csvfile:
            fieldnames = list(self.sensor.data.keys())
            writter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.readheadings():
                writter.writeheader()
            writter.writerow(self.sensor.data)
            csvfile.flush()

    def readheadings(self):
        """Read heading of csv file

        This method is used to read headings of the csv file to determine
        if new headings need to be written

        Returns:
            Bool: a boolean to check if new headings need to be written
        """
        with open (self.filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            try:
                i = next(reader)
                if i != list(self.sensor.data.keys()):
                    return True
            except StopIteration:
                print("Empty file")
                return True
            return False