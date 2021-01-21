import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
from tornado.concurrent import run_on_executor
from concurrent import futures

class WSHandler(tornado.websocket.WebSocketHandler):

    executor = futures.ThreadPoolExecutor(max_workers=1)

    def open(self):
        print("New connection")
        self.sensor_data_pull_method()

    def on_message(self, message):
        print("Message received")
        self.write_message(str('{"TestStr" : "Test", "TestNum" : "123"}'))

    def on_close(self):
        print("Connection closed")

    def check_origin(self, origin):
        return True

    #TODO parametarise sleep time and While True
    @run_on_executor
    def sensor_data_pull_method(self):
        while True:
            time.sleep(2)
            print("I am pulling")

application = tornado.web.Application([(r'/', WSHandler)])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()
