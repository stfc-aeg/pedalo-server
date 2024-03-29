"""
WSHandler - Websocket handler for server class

This module implements a handler that will be used within main server class
to manage websocket connections and message, map messages to functions, and
deal with wrong messages.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .server import Server
import tornado.websocket
import tornado.web
import json

class WSHandler(tornado.websocket.WebSocketHandler):
    """Message Handler

    This Class handles the messages from Scratch3 that it recives via
    Websocket. It has a dictionary of messages that acts like
    switch statement. Inherits from tornado.websocket.WebSocketHandler
    """
    def initialize(self, server):
        """Initialize method of tornado.websocket.WebSocketHandler

        Args:
            server (Server): Main server that will connect this handler and sensors together
        """
        self.server = server  # type: Server

    def open(self):
        """Method to execute when connection opens
        """
        self.server.logger.info("New connection")

    def on_message(self, message):
        """Method to execute when message is from Scratch is recvied

        Args:
            message (str): message from Scratch3 in JSON format
        """
        self.server.logger.info("Message received")
        self.message_handler(message)

    def on_close(self):
        """Message to execute when connection between server and Scratch3 is terminated
        """
        self.server.logger.info("Connection closed")

    def check_origin(self, origin):
        """Security method

        """
        return True

    def message_handler(self, message):
        """Handle messages from client

        This method will handle any messages that handler recives
        via websocket. If message received is not recognized "Wrong command"
        message will be sent back to client
        Args:
            message (JSON): message from Scratch3
        """
        # TODO handle not json method trap error
        message_from_clientJson = json.loads(message)
        if not "Args" in message_from_clientJson:
            message_from_clientJson["Args"] = []
        switch = {
            "get_temp_msg": self.get_temperature,
            "get_gas_r_msg": self.get_gas_resistance,
            "get_channels_msg": self.get_channels,
            "get_data_msg": self.get_data,
            "plot_graph_msg": self.plot_graph,
            "change_csv_setting": self.write_csv
        }
        func = switch.get(
            message_from_clientJson["Command"],
            lambda: self.bad_call)
        func(message_from_clientJson["Args"])

    def plot_graph(self, *args):
        """Test funciton to see if client can open a new broweser tab

        This method is used to test extra functionality on the client side.
        """
        self.write_message("Message back")

    def bad_call(self):
        """Send error message to client

        This method will be called if the command received was in wrong format,
        or it could be mapped to function.
        """
        self.write_message("Wrong command")

    def get_temperature(self, *args):
        """Send temperature back to client

        If temperature reading is not available (if sensors is not connected),
        "No such data available" message will be sent"
        """
        try:
            self.write_message(str(self.server.sensor.data["Temperature"]))
        except KeyError:
            self.write_message("No such data available")

    def get_gas_resistance(self, *args):
        """Return gas resistance

        This method is used to retrun gas resistance reading from sensor
        """
        try:
            self.write_message(str(self.server.sensor.data["Gas resistance"]))
        except KeyError:
            self.write_message("No such data available")

    def get_channels(self, *args):
        """Return sensor channels

        This methods returns all possbile sensor channels to Scratch3
        """
        dict = {'Keys' : list(self.server.sensor.data.keys())}
        self.write_message(str(dict))

    def get_data(self, *args):
        """Return any chanels data

        This method will return requested channel's data
        """
        try:
            self.write_message(str(self.server.sensor.data[args[0]]))
        except KeyError:
            self.write_message("No such data available")

    def write_csv(self,*args):
        if args[0]:
            self.server.write_csv_file = True
        elif args[0] == False:
            self.server.write_csv_file = False
        else:
            self.write_message("CSV file has not changed")
            return
        self.write_message("CSV file has not changed")

class ImgHandler(tornado.web.RequestHandler):
    """Image Handler

    This class is used to display graph image to user
    if he/she requests it in broweser.
    Inherits from tornado.websocket.WebSocketHandler
    """

    def initialize(self, server):
        """Init method

        This is init method to link server object

        Args:
            server (Server): Main server object
        """
        self.server = server  # type: Server

    def get(self):
        """HTTP get method

        This method is used to show graph image to the user.
        """
        self.set_header('Content-type', 'image/png')
        self.set_header('Content-length', len(self.server.graph_image))
        self.write(self.server.graph_image)

class graphHandler(tornado.web.RequestHandler):

    def initialize(self, server):
        """Init method

        This is init method to link server object

        Args:
            server (Server): Main server object
        """
        self.server = server  # type: Server

    def get(self):
        """HTTP get method

        This method is used to reader a graph page to the user.
        """
        self.render("graphTemplate.html", src='localhost:8888/image.png', items=list(self.server.sensor.data.keys())[1:])

    def put(self):
        """HTTP put method

        This method is used to chnage the desired graph reading.
        """
        self.server.reading=self.request.body.decode()

class listHandler(tornado.web.RequestHandler):
    """Image Handler

    This class is used to display graph image to user
    if he/she requests it in broweser.
    Inherits from tornado.websocket.WebSocketHandler
    """

    def initialize(self, server):
        """Init method

        This is init method to link server object

        Args:
            server (Server): Main server object
        """
        self.server = server  # type: Server
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Origin", "*")

    def get(self):
        """HTTP get method

        This method is used to show graph image to the user.
        """
        self.write({'Keys' : list(self.server.sensor.data.keys())})