from pymatriz.client_interface import ApiClient
from pymatriz.enums import Market
from pymatriz.rest_client import RestClient
from pymatriz.websocket_client import WebSocketClient
from pymatriz.globals import config


class MatrizAPIClient(ApiClient):
    """ Matriz API client
    """

    def __init__(self, **kwargs):
        """Initialization of the Client.
        :param config: Any
         """
        if "username" not in kwargs:
            raise Exception("Missing required parameter 'username'")

        if "password" not in kwargs:
            raise Exception("Missing required parameter 'username'")

        config["username"] = kwargs["username"]
        config["password"] = kwargs["password"]
        config["account"] = kwargs["account"] if "account" in kwargs else None

        super().__init__(config)

        self.rest_client = RestClient(self.config)
        self.ws_client = WebSocketClient(self.config)

    def connect(self):
        # Get auth token and other useful settings
        settings = self.rest_client.update_token()
        self.set_settings(settings)

        self.ws_client.connect()

    def market_data_subscription(self, tickers, **kwargs):
        self.rest_client.market_data_subscription(tickers, **kwargs)

    def get_daily_history(self, tickers, **kwargs):
        self.market_data_subscription(tickers, **kwargs)

        return self.rest_client.get_daily_history(tickers, **kwargs)

    def get_intraday_history(self, tickers, **kwargs):
        self.market_data_subscription(tickers, **kwargs)

        return self.rest_client.get_intraday_history(tickers, **kwargs)

    def get_market_data(self):
        self.market_data_subscription(self.settings["favorites"])
        return self.rest_client.get_market_data()

    def set_exception_handler(self, handler):
        super().set_exception_handler(handler)
        self.rest_client.set_exception_handler(handler)
        self.ws_client.set_exception_handler(handler)

    def add_market_data_handler(self, handler):
        super().add_market_data_handler(handler)
        self.rest_client.add_market_data_handler(handler)
        self.ws_client.add_market_data_handler(handler)

    def remove_market_data_handler(self, handler):
        super().remove_market_data_handler(handler)
        self.rest_client.remove_market_data_handler(handler)
        self.ws_client.remove_market_data_handler(handler)

    def add_error_handler(self, handler):
        super().add_error_handler(handler)
        self.rest_client.add_error_handler(handler)
        self.ws_client.add_error_handler(handler)

    def remove_error_handler(self, handler):
        super().remove_error_handler(handler)
        self.rest_client.remove_error_handler(handler)
        self.ws_client.remove_error_handler(handler)

    def get_all_instruments(self):
        return self.rest_client.get_all_instruments()

    def add_order_report_handler(self, handler):
        raise NotImplemented

    def remove_order_report_handler(self, handler):
        raise NotImplemented

    def set_settings(self, settings):
        super().set_settings(settings)
        self.rest_client.set_settings(settings)
        self.ws_client.set_settings(settings)

    def close(self):
        self.ws_client.close_connection()
