import random
import tornado.httpserver
import sys
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import csv
import json
from tornado.concurrent import run_on_executor
from concurrent import futures

class Server(tornado.web.Application):

    def __init__(self):
        self.executor = futures.ThreadPoolExecutor(max_workers=1)
        self.sensor_loaded = False
        self.load_sensors()
        self.temperature = 0
        handlers = [(r'/', WSHandler, dict(server = self))]
        super().__init__(handlers)
        self.sensor_data_pull_method()

    def load_sensors(self):
        try:
            import bme680
            sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
            sensor.set_temperature_oversample(bme680.OS_8X)
            sensor.set_filter(bme680.FILTER_SIZE_3)
        except:
            pass
        print("Sensors are loaded")

    def sensor_data_pull(self):
        if self.sensor_loaded:
            self.temperature = sensor.data.temperature
        else:
            self.temperature = str(random.randint(0,10))

    def getTemperature(self):
        return self.temperature

    #TODO parametarise sleep time and While True
    @run_on_executor
    def sensor_data_pull_method(self):
        # fieldnames = ["TestStr", "TestNum"]
        # writter = csv.DictWriter(self.f, fieldnames=fieldnames)
        # writter.writeheader()
        while True:
            self.sensor_data_pull()
            # writter.writerow({"TestStr" : "Test", "TestNum" : "123"})
            # self.f.flush()
            time.sleep(0.5)

class WSHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, server):
        self.server = server #type: Server

    def open(self):
        print("New connection")

    def on_message(self, message):
        print("Message received")
        self.messageHandler(message)

    def on_close(self):
        print("Connection closed")

    def check_origin(self, origin):
        return True

    def messageHandler(self, message):
        messageFromServerJson = json.loads(message)
        switch = {
            "Test Message" : self.TestMessage,
            "Set offset" : self.setOffsetTemp,
            "Get temperature" : self.getTemperature
        }
        func = switch.get(messageFromServerJson["Command"], lambda: "Invalid message")
        func(messageFromServerJson["Args"])

    def TestMessage(self, *args):
        self.write_message("Test Message")

    def setOffsetTemp(self, *args):
        print(args[0])
        self.write_message("Finished")

    def getTemperature(self, *args):
        self.write_message(self.server.getTemperature())

def main():
    application = Server()
    application.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
