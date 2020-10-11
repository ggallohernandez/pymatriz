from pymatriz import messages
from pymatriz.enums import FieldType, MessageType, Market, MarketDataEntry
import pandas as pd


class Client:

    def __init__(self, config, settings=None):
        self.config = config
        self.settings = settings

        # Handlers for incoming messages
        self.market_data_handlers = []
        self.order_report_handlers = []
        self.error_handlers = []
        self.exception_handler = None

    def set_settings(self, settings):
        self.settings = settings

    def add_market_data_handler(self, handler):
        """ Adds a new Market Data handler to the handlers list.

        :param handler: function that is going to be call when a new Market Data Message is received.
        :type handler: callable.
        """
        if handler not in self.market_data_handlers:
            self.market_data_handlers.append(handler)

    def remove_market_data_handler(self, handler):
        """ Removes the Market Data handler from the handler list.

        :param handler: function to be removed from the handler list.
        :type handler: callable.
        """
        if handler in self.market_data_handlers:
            self.market_data_handlers.remove(handler)

    def add_order_report_handler(self, handler):
        """ Adds a new Order Report handler to the handlers list.

        :param handler: function that is going to be call when a new Order Report Message is received.
        :type handler: callable.
        """
        if handler not in self.order_report_handlers:
            self.order_report_handlers.append(handler)

    def remove_order_report_handler(self, handler):
        """ Removes the Order Report handler from the handler list.

        :param handler: function to be removed from the handler list.
        :type handler: callable.
        """
        if handler in self.order_report_handlers:
            self.order_report_handlers.remove(handler)

    def add_error_handler(self, handler):
        """ Adds a new Error handler to the handlers list.

        :param handler: function that is going to be call when a new Error Message is received.
        :type handler: callable.
        """
        if handler not in self.error_handlers:
            self.error_handlers.append(handler)

    def remove_error_handler(self, handler):
        """ Removes the Error handler from the handler list.

        :param handler: function to be removed from the handler list.
        :type handler: callable.
        """
        if handler in self.error_handlers:
            self.error_handlers.remove(handler)

    def set_exception_handler(self, handler):
        """ Sets the Exception Handler.

        :param handler: function called when Exception is raised.
        :type handler: callable.
        """
        self.exception_handler = handler

    def on_message(self, message):
        """ Called when a new message is received through the connection.

        :param message: message received.
        :type message: str
        """
        try:
            if message != "pong":
                if "\n" in message:
                    for line in message.split("\n"):
                        if ";" in line:
                            msg = self.parse_message(line[0], line[2:])
                            if msg:
                                self.handle_message(msg)
                else:
                    msg = self.parse_message(message[0], message[2:])
                    if msg:
                        self.handle_message(msg)

        except Exception as e:
            self.on_exception(e)

    def handle_message(self, msg):
        try:

            # Checks if it is an error message
            if FieldType.Type.value in msg:
                # extract the message type.
                msg_type = msg[FieldType.Type.value]

                # Checks message type and call the correct handlers
                if msg_type == MessageType.MarketData.value:
                    for handler in self.market_data_handlers:
                        df = pd.DataFrame(msg, index=[0])
                        df = df.drop([FieldType.Type.value], axis=1)
                        # df.set_index([FieldType.SymbolId.value, FieldType.Time.Type])
                        handler(df)
                elif msg_type == MessageType.Book.value:
                    for handler in self.order_report_handlers:
                        df = pd.DataFrame(msg, index=[0])
                        df = df.drop([FieldType.Type.value], axis=1)
                        handler(df)
                elif msg_type == MessageType.ConnectionStatus.value:
                    # self.connected = msg[FieldType.Status]
                    pass
                else:
                    msg_type_not_supported = "Websocket: Message Type not Supported. Message: {msg}"
                    for handler in self.error_handlers:
                        handler(msg_type_not_supported.format(msg=msg))
            else:
                msg_not_supported = "Websocket: Message Supported. Message: {msg}"
                for handler in self.error_handlers:
                    handler(msg_not_supported.format(msg=msg))

        except Exception as e:
            self.on_exception(e)

    def parse_message(self, msg_type, payload):
        parser = self.config["message_parsers"].get(MessageType(msg_type))

        if parser:
            return parser.parse(payload)

        return False

    def on_exception(self, exception):
        """Called when an exception occurred within the client.

        :param exception: exception raised.
        :type exception: exception object
        """
        self.exception_handler(exception)

    def _url(self, path):
        raise NotImplementedError


class ApiClient(Client):
    def __init__(self, config, settings=None):
        super().__init__(config, settings)

    def build_instruments(self, tickers, **kwargs):
        market = kwargs["market"] if "markets" in kwargs else Market.MERVAL
        terms = kwargs["terms"] if "terms" in kwargs else [MarketDataEntry.TERM_48HS]

        has_to_append_market = market.value not in tickers[0]
        has_to_append_terms = MarketDataEntry.TERM_CI.value not in tickers[0] and \
                              MarketDataEntry.TERM_24HS.value not in tickers[0] and \
                              MarketDataEntry.TERM_48HS.value not in tickers[0]

        if has_to_append_market:
            if has_to_append_terms:
                instruments = [
                    messages.DOUBLE_QUOTES.format(item=
                                                  messages.INSTRUMENT_TERM.format(ticker=ticker,
                                                                                  market=market.value,
                                                                                  term=term.value))
                    for term in terms
                    for ticker in tickers
                ]
            else:
                instruments = [
                    messages.DOUBLE_QUOTES.format(item=
                                                  messages.INSTRUMENT.format(ticker=ticker,
                                                                             market=market.value))
                    for ticker in tickers
                ]
        else:
            instruments = [messages.DOUBLE_QUOTES.format(item=ticker) for ticker in tickers]

        return instruments

    def get_messages(self, message):
        messages = []
        try:
            if message != "pong":
                if "\n" in message:
                    for line in message.split("\n"):
                        if ";" in line:
                            messages.append(self.parse_message(line[0], line[2:]))
                else:
                    messages.append(self.parse_message(message[0], message[2:]))

            return messages
        except Exception as e:
            self.on_exception(e)

    def get_market_data(self):
        raise NotImplementedError

    def get_intraday_history(self, tickers, **kwargs):
        raise NotImplementedError

    def get_daily_history(self, tickers, **kwargs):
        raise NotImplementedError

    def get_all_instruments(self):
        raise NotImplementedError
