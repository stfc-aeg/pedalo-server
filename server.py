import random
import tornado.httpserver
import sys
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import csv
from tornado.concurrent import run_on_executor
from concurrent import futures

if (len(sys.argv) == 2):
    import bme680
    try:
        sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except IOError:
        sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

def sensor_data_pull():
    try:
        if sensor.get_sensor_data():
            dataFromSensorFunc = sensor.data.temperature
    except:
            dataFromSensorFunc = str(random.randint(0,10))
    return dataFromSensorFunc

class WSHandler(tornado.websocket.WebSocketHandler):

    executor = futures.ThreadPoolExecutor(max_workers=1)

    def open(self):
        print("New connection")
        self.f = open("test.csv", "a", newline='')
        self.sensor_data_pull_method()

    def on_message(self, message):
        print("Message received")
        self.messageHandler(message)

    def on_close(self):
        print("Connection closed")
        self.f.close()

    def check_origin(self, origin):
        return True

    def messageHandler(self, message):
        switch = {
            "Test Message" : self.TestMessage
        }
        func = switch.get(message, lambda: "Invalid message")
        func()

    def TestMessage(self):
        self.write_message("Test Message")


    #TODO parametarise sleep time and While True
    @run_on_executor
    def sensor_data_pull_method(self):
        fieldnames = ["TestStr", "TestNum"]
        writter = csv.DictWriter(self.f, fieldnames=fieldnames)
        writter.writeheader()
        while True:
            global dataFromSensor
            dataFromSensor = sensor_data_pull()
            writter.writerow({"TestStr" : "Test", "TestNum" : "123"})
            self.f.flush()
            time.sleep(0.5)

application = tornado.web.Application([(r'/', WSHandler)])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()
