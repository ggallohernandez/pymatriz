import logging
from http.client import HTTPConnection
import websocket
import datetime
import pandas as pd
from pymatriz.enums import MarketDataEntry, Market
from pymatriz.client import MatrizAPIClient

# Rest client HTTP messages logging, adjust to logging.ERROR if you want to see full HTTP messages
log = logging.getLogger('urllib3')
log.setLevel(logging.DEBUG)

# logging from urllib3 to console
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
log.addHandler(ch)

# print statements from `http.client.HTTPConnection` to console/stdout
HTTPConnection.debuglevel = 1

# Websocket message logging
websocket.enableTrace(True)

# Set Matriz platform credentials provided by your broker
# required
username = 'YOUR_USER@broker.com'
password = 'CHANGE_ME'

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

client = MatrizAPIClient(username=username, password=password)

client.add_market_data_handler(lambda msg: print(msg[(msg["sid"] == "MERV - XMEV - GGAL - 48hs")]) if len(msg[(msg["sid"] == "MERV - XMEV - GGAL - 48hs")]) > 0 else None)
client.set_exception_handler(lambda e: print(e))

client.connect()
df = client.get_daily_history(["GGAL", "SUPV"], terms=[MarketDataEntry.TERM_24HS, MarketDataEntry.TERM_48HS], market=Market.MERVAL, start_date=datetime.date(2020, 9, 14))

print(df)

client.close()
