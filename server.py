import logging
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.options
import time
import json
import tornado.log
from tornado.concurrent import run_on_executor
from concurrent import futures
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
        """Configures loggers

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
        try:
            self.sensor = bme680sensor.bme680sensor()
        except sensorInterface.sensor_not_found:
            self.logger.warning("bme680 failed to load")
        try:
            self.sensor = bme280sensor.bme280sensor()
        except sensorInterface.sensor_not_found:
            self.logger.warning("bme280 failed to load")
        try:
            self.sensor = ds18b20sensor.ds18b20sensor()
        except sensorInterface.sensor_not_found:
            self.logger.warning("ds18b20sensor failed to load")
        try:
            self.sensor = enviroplussensor.enviroplussensor()
        except sensorInterface.sensor_not_found:
            self.logger.warning("enviroplussensor failed to load")

        if self.sensor == None:
            self.logger.warning("No sensors loaded")
            self.sensor = sensorInterface.Sensor()
            self.logger.info("Using sensor interface")

    def sensor_data_pull(self):
        """Pulling data from sensor

        This method accesses sensor's method to pull data from sensor
        """
        self.sensor.pull_data()

    # TODO parametarise sleep time and While True
    @run_on_executor
    def sensor_data_pull_method(self):
        # fieldnames = ["TestStr", "TestNum"]
        # writter = csv.DictWriter(self.f, fieldnames=fieldnames)
        # writter.writeheader()
        while self.pull_data:
            self.sensor_data_pull()
            # writter.writerow({"TestStr" : "Test", "TestNum" : "123"})
            # self.f.flush()
            time.sleep(self.sleep_time)


class WSHandler(tornado.websocket.WebSocketHandler):
    """Message Handler

    This Class handles the messages from Scratch3 that it recives via
    Webscoket. It has a dictionary of messages that acts like
    switch statement.

    Args:
        tornado (tornado.websocket.WebSocketHandler): Base tornado handler
    """

    def initialize(self, server):
        self.server = server  # type: Server

    def open(self):
        self.server.logger.info("New connection")

    def on_message(self, message):
        self.server.logger.info("Message received")
        self.message_handler(message)

    def on_close(self):
        self.server.logger.info("Connection closed")

    def check_origin(self, origin):
        return True

    def message_handler(self, message):
        """Message handler mathod

        This method will handle any messages that handler recives
        via websocket. This method maps messages to methods within
        handler class.
        Args:
            message (JSON): message from Scratch3
        """
        message_from_serverJson = json.loads(message)
        switch = {
            "test_msg": self.test_message,
            "set_off_set_msg": self.set_offset_temp,
            "get_temp_msg": self.get_temperature,
            "get_gas_r_msg": self.get_gas_resistance,
            "get_channels_msg": self.get_channels,
            "get_data_msg": self.get_data
        }
        func = switch.get(
            message_from_serverJson["Command"],
            lambda: "Invalid message")
        func(message_from_serverJson["Args"])

    def test_message(self, *args):
        self.write_message("Test Message")

    def set_offset_temp(self, *args):
        self.server.logger.debug(args[0])
        self.write_message("Finished")

    def get_temperature(self, *args):
        self.write_message(str(self.server.sensor.data["Temperature"]))

    def get_gas_resistance(self, *args):
        self.write_message(str(self.server.sensor.data["Gas resistance"]))

    def get_channels(self, *args):
        self.write_message(str(list(self.server.sensor.data.keys())))

    def get_data(self, *args):
        try:
            self.write_message(str(self.server.sensor.data[args[0]]))
        except KeyError:
            self.write_message("No such data available")


def main():
    application = Server()
    application.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
