"""Server - Main class of the application

This module implements server class that will allow sensors and
websocket to communicate. Main functionality of this class is to run a
server with websocket handler and to load sensors so they can be used by pulling
data from them.

Vladimir Garanin, STFC Detector Systems Software Group
"""
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import time
import tornado.log
from tornado.concurrent import run_on_executor
from concurrent import futures
from .handlers import WSHandler
import sensorInterface
import bme680sensor
import bme280sensor
import ds18b20sensor
import enviroplussensor


class Server(tornado.web.Application):
    """Class to manage the application and establish communication to sensors

    Args:
        tornado (tornado.web.Application): Base application class
    """
    def __init__(self):
        # TODO NEEDS DOCSTRING
        """[summary]
        """
        self.init_logger()
        self.executor = futures.ThreadPoolExecutor(max_workers=1)
        self.sensor = None
        self.load_sensors()
        self.pull_data = True
        self.sleep_time = 0.5
        handlers = [(r'/', WSHandler, dict(server=self))]
        super().__init__(handlers)
        self.sensor_data_pull_method()

    def init_logger(self):
        """Configure logger

        This method configures loggers to be used in the application
        """
        tornado.options.parse_command_line()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.DEBUG)

    def load_sensors(self):
        """Load sensor classes

        This method loads sensor code into the application, this
        method will try to load all known sensor, however only one
        of them will be used
        """
        # TODO take away failed and replace with not found
        try:
            self.sensor = bme680sensor.bme680sensor()
        except sensorInterface.sensor_not_found:
            self.logger.info("bme680 failed to load")
        try:
            self.sensor = bme280sensor.bme280sensor()
        except sensorInterface.sensor_not_found:
            self.logger.info("bme280 failed to load")
        try:
            self.sensor = ds18b20sensor.ds18b20sensor()
        except sensorInterface.sensor_not_found:
            self.logger.info("ds18b20sensor failed to load")
        try:
            self.sensor = enviroplussensor.enviroplussensor()
        except sensorInterface.sensor_not_found:
            self.logger.info("enviroplussensor failed to load")

        if self.sensor == None:
            self.logger.warning("No sensors loaded")
            self.sensor = sensorInterface.Sensor()
            self.logger.info("Using sensor interface")

    def sensor_data_pull(self):
        """Pull data from sensor

        This method accesses sensor's method to pull data from sensor
        """
        self.sensor.pull_data()

    # TODO implement writing to csv file
    # TODO only write subset of data to csv
    # TODO But pull every second
    @run_on_executor
    def sensor_data_pull_method(self):
        """Write to cvs file

        This methods will write all data to csv file every ""self.sleep_time"
        """
        # fieldnames = ["TestStr", "TestNum"]
        # writter = csv.DictWriter(self.f, fieldnames=fieldnames)
        # writter.writeheader()
        while self.pull_data:
            self.sensor_data_pull()
            # writter.writerow({"TestStr" : "Test", "TestNum" : "123"})
            # self.f.flush()
            time.sleep(self.sleep_time)
# TODO docstring
def main():
    application = Server()
    application.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
