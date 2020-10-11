"""
    Defines library global variables
"""
from pymatriz.enums import MessageType
from pymatriz.parser import MarketDataMessageParser, BookMessageParser, ConnectionStatusMessageParser

config = {
    "ssl": True,
    "url": "https://mtzdma.primary.ventures/",
    "ws_url": "wss://mtzdma.primary.ventures/",
    "message_parsers": {
        MessageType.MarketData: MarketDataMessageParser,
        MessageType.Book: BookMessageParser,
        MessageType.Portfolio: None,
        MessageType.Order: None,
        MessageType.OrderEvent: None,
        MessageType.News: None,
        MessageType.ExternalMarketData: None,
        MessageType.ConnectionStatus: ConnectionStatusMessageParser,
        MessageType.Clock: None,
        MessageType.CancelReject: None,
        MessageType.Control: None,
        MessageType.Ignore: None,
    }
}