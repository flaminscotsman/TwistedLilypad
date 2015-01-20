from struct import unpack_from, calcsize

from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder, varIntPrefixedStringListEncoder


class RequestNotifyPlayer(AbstractRequest):
    opcode = 0x21

    def __init__(self, add, player):
        self.add = add
        self.player = player


class RequestNotifyPlayerCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestNotifyPlayer)

        return booleanEncoder(request.add) + varIntPrefixedStringListEncoder(request.player)

    @staticmethod
    def decode(payload):
        add = unpack_from('>B', payload) == 0
        payload = payload[calcsize('>B'):]
        player, payload = varIntPrefixedStringParser(payload)
        return RequestNotifyPlayer(add, player)