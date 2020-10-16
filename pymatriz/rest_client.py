import csv
from collections import defaultdict
from datetime import datetime, timedelta

import pandas as pd
from io import StringIO

import requests
import logging
from http.client import HTTPConnection  # py3
from lxml import html
import re
import base64
import json

from pymatriz import urls, messages
from pymatriz.client_interface import ApiClient
from pymatriz.enums import Market, FieldType, HistoryFieldType
from pymatriz.exceptions import ApiException


class RestClient(ApiClient):
    """ Rest client that implements call to Matriz Rest API
    """

    def __init__(self, config):
        """Initialization of the Client.
        :param config: Any
        """
        super().__init__(config)

        # self.log = logging.getLogger('urllib3')
        # self.log.setLevel(logging.ERROR)
        #
        # # logging from urllib3 to console
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.ERROR)
        # self.log.addHandler(ch)
        #
        # # print statements from `http.client.HTTPConnection` to console/stdout
        # HTTPConnection.debuglevel = 0

        self.session = requests.Session()

    def update_token(self):
        """Get Matriz settings object, which contains useful data like web token, websocket connection id, RIMA web token.
        :return: Any
        """
        username = self.config["username"]
        password = self.config["password"]

        # Matriz Web Platform Auth0 client ID
        client_id = "LlRkDft0IVkhGLXoknIaOtvlcc7eVAfX"
        auth0_api_id = "matriz.auth0.com"
        auth0_client = "eyJuYW1lIjoibG9jay5qcyIsInZlcnNpb24iOiIxMS41LjIiLCJsaWJfdmVyc2lvbiI6IjkuNC4yIn0="
        realm = "dma3-prod-db"
        credential_type = "http://auth0.com/oauth/grant-type/password-realm"

        matriz_url = "https://mtzdma.primary.ventures"
        redirect_uri = "https://mtzdma.primary.ventures/auth/auth0/callback"

        # Get Auth0 Login ticket
        payload = json.dumps({
            "client_id": client_id,
            "username": username,
            "password": password,
            "realm": realm,
            "credential_type": credential_type
        })

        headers = {
            'authority': auth0_api_id,
            'auth0-client': auth0_client,
            'origin': matriz_url,
            'referer': matriz_url,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'Content-Type': 'application/json',
        }

        response = self.session.request("POST", urls.authenticate, headers=headers, data=payload)

        # Get Auth0 Access token
        url = urls.authorize.format(client_id=client_id,
                                    response_type="token",
                                    response_mode="form_post",
                                    redirect_uri=redirect_uri,
                                    connection=realm,
                                    realm=realm,
                                    scope="openid profile email",
                                    login_ticket=response.json()["login_ticket"],
                                    auth0_client=auth0_client)

        payload = {}
        headers = {
            'authority': auth0_api_id,
            'upgrade-insecure-requests': '1',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': matriz_url,
        }

        response = self.session.request("GET", url, headers=headers, data=payload)
        root = html.fromstring(response.text.encode('utf8'))

        # Get Matriz Platform settings object
        payload = dict(map(lambda i: (i.name, i.value), root.xpath("//form/input")))

        response = self.session.post(root.xpath("//form")[0].action, data=payload)

        settings = json.loads(base64.b64decode(re.search("var settings = '(.*)'", response.text).groups()[0]))

        self.settings = settings

        return settings

    def get_market_data(self):
        response = self.api_request(urls.market_data)

        df = pd.DataFrame(self.get_messages(response.text))

        df = df.drop([FieldType.Type.value], axis=1)

        return df

    def get_intraday_history(self, tickers, **kwargs):
        return self._get_history_call(urls.historical_series_intraday, tickers, **kwargs)

    def get_daily_history(self, tickers, **kwargs):
        return self._get_history_call(urls.historical_series_daily, tickers, **kwargs)

    def _get_history_call(self, url_template, tickers, **kwargs):
        responses = []

        start_date = datetime.fromordinal(kwargs["start_date"].toordinal()).isoformat("T") + "Z" \
            if "start_date" in kwargs else (datetime.utcnow() - timedelta(days=1)).isoformat("T") + "Z"
        end_date = datetime.fromordinal(kwargs["end_date"].toordinal()).isoformat("T") + "Z" \
            if "end_date" in kwargs else (datetime.utcnow() + timedelta(days=1)).isoformat("T") + "Z"

        instruments = self.build_instruments(tickers, **kwargs)

        for instrument in instruments:
            url = url_template.format(instrument=instrument.strip('"'), start_date=start_date, end_date=end_date)
            response = self.api_request(url)

            content = response.content.decode('utf-8')
            r = pd.read_csv(StringIO(content), sep=",")
            r.insert(0, HistoryFieldType.SymbolId.value, instrument.strip('"'))
            responses.extend(r.to_dict(orient='records'))

        df = pd.DataFrame(responses)

        if len(df) > 0:
            index = []

            if HistoryFieldType.SymbolId.value in df:
                index.append(HistoryFieldType.SymbolId.value)

            if HistoryFieldType.Time.value in df:
                index.append(HistoryFieldType.Time.value)

            df.set_index(index, inplace=True)

        return df

    def get_all_instruments(self):
        """Make a request to the API and get a list of all available instruments.

        For more detailed information go to: https://apihub.primary.com.ar/assets/docs/Primary-API.pdf

        :return: A list of valid instruments returned by the API.
        :rtype: dict of JSON response.
        """
        response = self.api_request(urls.instruments)

        return pd.DataFrame(json.loads(response.text))

    def market_data_subscription(self, tickers, **kwargs):
        """ Creates and sends new Market Data Subscription Message through the connection.

        :param tickers: List of the tickers to subscribe.
        :type tickers: list of str
        :param market: Market id associated to the tickers.
        :type market: Market (Enum).
        :param terms: List of terms that want to be received.
        Example: [MarketDataEntry.TERM_CI, MarketDataEntry.TERM_24HS]
        :type terms: List of MarketDataEntry (Enum).
        """

        # Iterates through the tickers list and creates a new list of Instrument String using the INSTRUMENT Template.
        # Then create a comma separated string with the instruments in the list.
        instruments = self.build_instruments(tickers, **kwargs)

        instruments_string = ",".join(instruments)

        # Creates a Market Data Subscription Message using the Template.
        message = messages.MARKET_DATA_SUBSCRIPTION.format(instruments=instruments_string)

        # Send the message through the connection.
        response = self.api_post(urls.ws_subscribe.format(token=self.settings["token"], connection_id=self.settings["connId"]), message)

    def api_request(self, path, retry=True):
        """ Make a GET request to the API.
        :param path: path to the API resource.
        :type path: str
        :param retry: (optional) True: update the token and resend the request if the response code is 401.
        False: raise an exception if the response code is 401.
        :type retry: str
        :return: response of the API.
        :rtype: Response
        """
        headers = {'authorization': f'Bearer {self.settings["token"]}'}
        response = self.session.get(self._url(path),
                                    headers=headers,
                                    verify=self.config["ssl"] if "ssl" in self.config else True,
                                    proxies=self.config["proxies"] if "proxies" in self.config else None)

        # Checks if the response code is 401 (Unauthorized)
        if response.status_code == 401:
            if retry:
                self.update_token()
                self.api_request(path, False)
            else:
                raise ApiException("Authentication Fails.")
        elif response.status_code < 200 or response.status_code > 299:
            raise ApiException(f"Failure requesting {path}. Response ({response.status_code}): {response.text}")

        return response

    def api_post(self, path, data, retry=True):
        """ Make a POST request to the API.
        :param path: path to the API resource.
        :type path: str
        :param retry: (optional) True: update the token and resend the request if the response code is 401.
        False: raise an exception if the response code is 401.
        :type retry: str
        :return: response of the API.
        :rtype: Response
        """
        headers = {'authorization': f'Bearer {self.settings["token"]}', 'Origin': self.config["url"], 'content-type': 'application/json', 'x-csrf-token': self.settings["csrfToken"]}
        response = self.session.post(self._url(path),
                                     data,
                                     headers=headers,
                                     verify=self.config["ssl"] if "ssl" in self.config else True,
                                     proxies=self.config["proxies"] if "proxies" in self.config else None)

        # Checks if the response code is 401 (Unauthorized)
        if response.status_code == 401:
            if retry:
                self.update_token()
                self.api_post(path, data, False)
            else:
                raise ApiException("Authentication Fails.")
        elif response.status_code < 200 or response.status_code > 299:
            raise ApiException(f"Failure requesting {path}. Response ({response.status_code}): {response.text}")

        return response

    def _url(self, path):
        """ Helper function that concatenate the path to the API url.
        :param path: path to the API resource.
        :type path: str
        :return: URL to be call.
        :rtype: str
        """
        return self.config["url"] + path
