"""
    Defines APIs messages templates
"""

# Template for a Market Data Subscription message
MARKET_DATA_SUBSCRIPTION = '{{"md":[{instruments}],"book":[{instruments}]}}'

# Template to specify an instrument in a market data subscription message
INSTRUMENT = "{market} - {ticker}"
INSTRUMENT_TERM = "{market} - {ticker} - {term}"

# Template to insert a Double Quote
DOUBLE_QUOTES = '"{item}"'

PING = "ping"
REQUEST = "k;request"
