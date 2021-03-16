import logging
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import json
import tornado.log
from tornado.concurrent import run_on_executor
from concurrent import futures
import sensorInterface
import bme680sensor
import bme280sensor
import ds18b20sensor


class Server(tornado.web.Application):
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
        self.logger = logging.getLogger("Server")
        self.logger.propagate = False
        file_logger_handler = logging.FileHandler("log.txt")
        console_logger_handler = logging.StreamHandler()
        formater = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_logger_handler.setFormatter(formater)
        file_logger_handler.setLevel(logging.INFO)
        console_logger_handler.setFormatter(formater)
        console_logger_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_logger_handler)
        self.logger.addHandler(console_logger_handler)
        self.logger.setLevel(logging.DEBUG)

    def load_sensors(self):
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

        if self.sensor == None:
            self.logger.warning("No sensors loaded")
            self.sensor = sensorInterface.Sensor()
            self.logger.info("Using sensor interface")

    def sensor_data_pull(self):
            self.sensor.pull_data()

    def get_temperature(self):
        if self.fahrenheit:
            return (self.temperature * 9/5 + 32)
        else:
            return self.temperature

    def to_fahrenheit(self):
        self.fahrenheit = True

    # TODO parametarise sleep time and While True
    @run_on_executor
    def sensor_data_pull_method(self):
        # fieldnames = ["TestStr", "TestNum"]
        # writter = csv.DictWriter(self.f, fieldnames=fieldnames)
        # writter.writeheader()
        while self.pull_data:
            self.sensor_data_pull()
            self.logger.debug(list(self.sensor.data.keys()))
            # writter.writerow({"TestStr" : "Test", "TestNum" : "123"})
            # self.f.flush()
            time.sleep(self.sleep_time)


class WSHandler(tornado.websocket.WebSocketHandler):

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
