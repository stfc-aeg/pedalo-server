import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print("New connection")

    def on_message(self, message):
        print("Message received")
        self.write_message(str('{"TestStr" : "Test", "TestNum" : "123"}'))

    def on_close(self):
        print("Connection closed")

    def check_origin(self, origin):
        return True

application = tornado.web.Application([(r'/', WSHandler)])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    print("*** Websocket Server Started")
    tornado.ioloop.IOLoop.instance().start()
