from tornado import httputil
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import csv
from tornado.concurrent import run_on_executor
from concurrent import futures

class WSHandler(tornado.websocket.WebSocketHandler):

    executor = futures.ThreadPoolExecutor(max_workers=1)

    def open(self):
        print("New connection")
        self.f = open("test.csv", "a", newline='')
        self.sensor_data_pull_method()

    def on_message(self, message):
        print("Message received")
        self.write_message(str('{"TestStr" : "Test", "TestNum" : "123"}'))

    def on_close(self):
        print("Connection closed")
        self.f.close()

    def check_origin(self, origin):
        return True

    #TODO parametarise sleep time and While True
    @run_on_executor
    def sensor_data_pull_method(self):
        fieldnames = ["TestStr", "TestNum"]
        writter = csv.DictWriter(self.f, fieldnames=fieldnames)
        writter.writeheader()
        while True:
            writter.writerow({"TestStr" : "Test", "TestNum" : "123"})
            self.f.flush()
            time.sleep(2)

application = tornado.web.Application([(r'/', WSHandler)])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()
