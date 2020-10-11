# -*- coding: utf-8 -*-
"""
    pyRofex.websocket_client

    Defines a Websocket Client that connect to ROFEX Websocket API.
"""
import logging
import threading
import time

import websocket

from pymatriz import urls, messages
from pymatriz.client_interface import Client
from pymatriz.enums import MessageType, FieldType, Market
from pymatriz.exceptions import ApiException
from pymatriz.parser import MarketDataMessageParser, BookMessageParser
from pymatriz.utils import set_interval


class WebSocketClient(Client):
    """ Websocket Client that connect to Primary Websocket API.

    This client used a websocket implementation of the library websocket_client.

    - For more references of websocket_client library go to: https://pypi.org/project/websocket_client
    - For more information about the API go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

    """

    def __init__(self, config):
        """ Initialization of the client.

        Create and initialize instance variables for the client.

        :param config: Any
        """
        super().__init__(config)

        self._PING_INVERVAL = 30

        # Connection related variables
        self.ws_connection = None
        self.ws_thread = None
        self.connected = False

    def connect(self):
        """ Start a new websocket connection with Matriz API.

        Create an instance WebSocketApp using the environment
        It will create a new thread that is going to be listening new incoming messages.
        """
        url = self._url(urls.ws_request.format(token=self.settings["token"],
                                               connection_id=self.settings["connId"],
                                               account=self.config["account"] or self.settings["defaultAccount"]))


        # websocket.enableTrace(False)

        self.ws_connection = websocket.WebSocketApp(url,
                                                    on_message=self.on_message,
                                                    on_error=self.on_error,
                                                    on_close=self.on_close,
                                                    on_open=self.on_open)

        # Create a thread and target it to the run_forever function, then start it.
        self.ws_thread = threading.Thread(target=self.ws_connection.run_forever,
                                          kwargs={"ping_interval": self._PING_INVERVAL})
        self.ws_thread.start()

        # Wait 5 sec to establish the connection
        conn_timeout = 5
        time.sleep(1)
        while not self.ws_connection.sock.connected and conn_timeout:
            time.sleep(1)
            conn_timeout -= 1
        if not self.ws_connection.sock.connected:
            self.on_exception(ApiException("Connection could not be established."))

    def on_error(self, exception):
        """ Called when an error occurred within the connection.

        :param exception: exception raised.
        :type exception: exception object
        """
        self.ws_connection.close()
        self.on_exception(exception)

    def on_close(self):
        """ Called when the connection was closed.
        """
        self.connected = False

    def on_open(self):
        """ Called when the connection was opened.
        """
        self.connected = True

        # self.ping_timer = set_interval(self._PING_INVERVAL, self.ping)

        # r = threading.Timer(1.0, self.ws_connection.send, messages.REQUEST)
        # r.start()

    def ping(self):
        self.ws_connection.send(messages.PING)

    def close_connection(self):
        """ Close the connection.
        """
        # self.ping_timer.cancel()
        self.ws_connection.close()

    # def order_report_subscription(self, account, snapshot):
    #     """ Creates and sends new Order Report Subscription Message through the connection.
    #
    #     :param account: account that will be send in the message.
    #     :type account: str.
    #     :param snapshot: True: old Order Reports won't be received; False: old Order Report will be received.
    #     :type snapshot: boolean.
    #     """
    #
    #     # Create an Order Subscription message using the Template and the parameters.
    #     message = messages.ORDER_SUBSCRIPTION.format(a=account, snapshot=snapshot.__str__().lower())
    #
    #     # Send the message through the connection.
    #     self.ws_connection.send(message)

    def is_connected(self):
        """ Checks if the client is connected to the API.

        :return: True: if it is connected. False: if it is not connected.
        :rtype: boolean.
        """
        return self.connected

    def _url(self, path):
        """ Helper function that concatenate the path to the API url.
        :param path: path to the API resource.
        :type path: str
        :return: URL to be call.
        :rtype: str
        """
        return self.config["ws_url"] + path
