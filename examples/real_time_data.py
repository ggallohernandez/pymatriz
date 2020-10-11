import datetime
import pandas as pd
from pymatriz.enums import MarketDataEntry, Market
from pymatriz.client import MatrizAPIClient

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

client.market_data_subscription(["GGAL"], terms=[MarketDataEntry.TERM_48HS], market=Market.MERVAL)

# Call to disconnect from websocket
# client.close()
