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

client.connect()

df = client.get_daily_history(["GGAL", "SUPV"], terms=[MarketDataEntry.TERM_24HS, MarketDataEntry.TERM_48HS], start_date=datetime.date(2020, 9, 14))

print(df)

client.close()
