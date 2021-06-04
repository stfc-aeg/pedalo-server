"""Server - Main class of the application

This module implements server class that will allow sensors and
websocket to communicate. Main functionality of this class is to run a
server with websocket handler and to load sensors so they can be used by pulling
data from them.

Vladimir Garanin, STFC Detector Systems Software Group
"""
import collections
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import time
import tornado.log
from tornado.concurrent import run_on_executor
from concurrent import futures
from .graph import Graphplot
from .csvhandler import Csvfilehandler
from .handlers import WSHandler, ImgHandler, graphHandler, listHandler
from .sensors.bme280 import bme280sensor 
from .sensors.ds18b20 import ds18b20sensor 
from .sensors.enviroplus import enviroplussensor 
from .sensors.bme680 import bme680sensor
from .sensors.sensor import sensor_not_found


class Server(tornado.web.Application):
    """Class to manage the application and establish communication to sensors

    Args:
        tornado (tornado.web.Application): Base application class
    """
    def __init__(self):
        """Initiate server object

        This is initiate method which creates logger, initiates sensors
        and attaches server handler.
        """
        self.init_logger()
        self.executor = futures.ThreadPoolExecutor(max_workers=2)
        self.load_sensors()
        self.csvfile = Csvfilehandler("testing.csv",self.sensor)
        self.reading = "Temperature"
        self.graph = Graphplot(self)
        self.pull_data = True
        self.sleep_time = 1
        self.write_csv_file = True
        handlers = [(r'/', WSHandler, dict(server=self)),
                    (r'/image.png', ImgHandler, dict(server=self)),
                    (r'/graph', graphHandler, dict(server=self)),
                    (r'/list', listHandler, dict(server=self))]
        super().__init__(handlers)
        self.sensor_data_pull_method()
        self.sensor_data_plot_method()

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
        self.sensor = None
        try:
            self.sensor = bme680sensor()
        except sensor_not_found:
            self.logger.info("bme680 not found")
        try:
            self.sensor = bme280sensor()
        except sensor_not_found:
            self.logger.info("bme280 not found")
        try:
            self.sensor = ds18b20sensor()
        except sensor_not_found:
            self.logger.info("ds18b20sensor not found")
        try:
            self.sensor = enviroplussensor()
        except sensor_not_found:
            self.logger.info("enviroplussensor not found")

    def sensor_data_pull(self):
        """Pull data from sensor

        This method accesses sensor's method to pull data from sensor
        """
        if self.sensor:
            self.sensor.pull_data()

    @run_on_executor
    def sensor_data_pull_method(self):
        """Write to cvs file

        This methods will write all data to csv file every "counter" second
        This method also saves data from sensor to in memeory queue so it can be
        used to plot a graph.

        """
        counter = 0
        self.data_in_memory = collections.deque([],100)
        while True:
            self.sensor_data_pull()
            try:
                self.data_in_memory.append(self.sensor.data.copy())
            except IndexError:
                self.data_in_memory.popleft()
                self.data_in_memory.append(self.sensor.data.copy())
            counter +=1
            if counter == 5 and self.write_csv_file:
                counter = 0
                self.csvfile.writetofile()
                self.logger.debug("Csv file written")
            elif counter == 5:
                counter = 0
            time.sleep(self.sleep_time)

    @run_on_executor
    def sensor_data_plot_method(self):
        while True:
            self.graph_image = self.graph.plotgraph(self.data_in_memory)
            self.logger.debug("Graph plotted")
            time.sleep(self.sleep_time)

def main():
    """Start server

    This is main function that creates server object and sets it on port 8888
    """
    application = Server()
    application.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()
