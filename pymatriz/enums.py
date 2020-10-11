from enum import Enum


class Market(Enum):
    """Market ID associated to the instruments.
    ROFEX: ROFEX Exchange.
    """
    ROFEX = 'ROFX'
    MERVAL = 'MERV - XMEV'


class MarketDataEntry(Enum):
    TERM_CI = 'CI'
    TERM_24HS = '24hs'
    TERM_48HS = '48hs'


class MessageType(Enum):
    MarketData = 'm'
    Book = 'b'
    Portfolio = 'p'
    Order = 'o'
    OrderEvent = 'e'
    News = 'n'
    ExternalMarketData = 'x'
    ConnectionStatus = 'c'
    Clock = 'k'
    CancelReject = 'r'
    Control = '$'
    Ignore = '_'


class HistoryFieldType(Enum):
    SymbolId = 'sid'
    Time = 'time'
    OpeningPrice = 'open'
    ClosingPrice = 'close'
    LowPrice = 'low'
    HighPrice = 'high'
    TradeVolume = 'volume'


class FieldType(Enum):
    SymbolId = 'sid'
    Seq = 'seq'
    Offers = 'ask'
    Asz = 'asz'
    Bids = 'bid'
    Bsz = 'bsz'
    Last = 'lst'
    OpeningPrice = 'opn'
    ClosingPrice = 'cls'
    LowPrice = 'low'
    HighPrice = 'hgh'
    NominalVolume = 'von'
    TradeVolume = 'vol'
    Time = 'hor'
    SettlementPrice = 'set'
    OpenInterest = 'oin'
    Refp = 'refp'

    Type = 'type'
    Books = 'books'
    Status = 'status'

    # get_all_instruments
    Aon = 'aon'  # false
    Cfi = 'cfi'  # "ESXXXX"
    Currency = 'cur'  # "ARS"
    Decimals = 'dec'  # 3
    Description = 'des'  # "Rigolleau"
    Exp = 'exp'  # null
    Fix = 'fix'  # "MERV - XMEV - RIGO - 24hs"
    Fun = 'fun'  # "Rigolleau Merval"
    Grp = 'grp'  # null
    Hid = 'hid'  # true
    Iso = 'iso'  # 0
    Isu = 'isu'  # 0
    Mdet = 'mdet'  # "0124578Cxw"
    Market = 'mkt'  # "bm"
    Mpt = 'mpt'  # 0.1
    Mst = 'mst'  # 1
    Ord = 'ord'  # 1
    Prd = 'prd'  # null
    Pxq = 'pxq'  # 1
    Sdc = 'sdc'  # 0
    Segment = 'seg'  # "bm_MERV"
    Ser = 'ser'  # "RIGO"
    Srt = 'srt'  # "bm:RIGO:c:24hs"
    Str = 'str'  # null
    Symbol = 'sym'  # "RIGO (24hs)"
    TypeAcronym = 'typ'  # null
    Und = 'und'  # "MERV - XMEV - RIGO - 48hs"
    Vtm = 'vtm'  # null
    Vty = 'vty'  # null
