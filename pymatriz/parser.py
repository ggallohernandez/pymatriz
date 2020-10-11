from pymatriz.enums import FieldType, MessageType
from pymatriz.exceptions import ParsingException


class MessageParser:
    @staticmethod
    def parse(message):
        raise NotImplementedError


class MarketDataMessageParser(MessageParser):

    _MD_FIELDS = 17

    @staticmethod
    def parse(message):
        fields = message.split("|")

        if len(fields) < MarketDataMessageParser._MD_FIELDS:
            raise ParsingException(f"Invalid tick length: {len(fields)}.")

        return {
            FieldType.Type.value: MessageType.MarketData.value,
            FieldType.SymbolId.value: fields[0],
            FieldType.Seq.value: fields[1],
            FieldType.Offers.value: fields[2] if fields[2] != "" else None,
            FieldType.Asz.value: fields[3] if fields[3] != "" else None,
            FieldType.Bids.value: fields[4] if fields[4] != "" else None,
            FieldType.Bsz.value: fields[5] if fields[5] != "" else None,
            FieldType.Last.value: fields[6] if fields[6] != "" else None,
            FieldType.OpeningPrice.value: fields[7] if fields[7] != "" else None,
            FieldType.ClosingPrice.value: fields[8] if fields[8] != "" else None,
            FieldType.LowPrice.value: fields[9] if fields[9] != "" else None,
            FieldType.HighPrice.value: fields[10] if fields[10] != "" else None,
            FieldType.NominalVolume.value: fields[11] if fields[11] != "" else None,
            FieldType.TradeVolume.value: fields[12] if fields[12] != "" else None,
            FieldType.Time.value: fields[13],
            FieldType.SettlementPrice.value: fields[14] if fields[14] != "" else None,
            FieldType.OpenInterest.value: fields[15] if fields[15] != "" else None,
            FieldType.Refp.value: fields[16] if fields[16] != "" else None
        }


class BookMessageParser(MessageParser):

    _BOOK_FIELDS = 5

    @staticmethod
    def parse(message):
        message_fields = message.split("!")

        if len(message_fields) < BookMessageParser._BOOK_FIELDS:
            raise ParsingException(f"Invalid tick length: {len(message_fields)}.")

        sid = message_fields[0]
        seq = message_fields[1]
        books = []

        for content in message_fields[2:5]:
            fields = content.split("|")

            books.append({
                FieldType.Bsz.value: fields[0] if fields[0] != "" else None,
                FieldType.Bids.value: fields[1] if fields[1] != "" else None,
                FieldType.Offers.value: fields[2] if fields[2] != "" else None,
                FieldType.Asz.value: fields[3] if fields[3] != "" else None,
            })

        return {
            FieldType.Type.value: MessageType.Book.value,
            FieldType.SymbolId.value: sid,
            FieldType.Seq.value: seq,
            FieldType.Books.value: books
        }


class ConnectionStatusMessageParser(MessageParser):
    @staticmethod
    def parse(message):
        return {
            FieldType.Type.value: MessageType.ConnectionStatus.value,
            FieldType.Status.value: "connected" == message
        }
