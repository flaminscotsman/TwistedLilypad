from struct import unpack_from, calcsize

from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec
from twistedlilypad.utilities import boolean_encoder, varint_prefixed_string_encoder, varint_prefixed_string_parser


class RequestNotifyPlayer(AbstractRequest):
    opcode = 0x21

    def __init__(self, joining, player):
        self.joining = joining
        self.player = player


class RequestNotifyPlayerCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        return boolean_encoder(request.joining) + varint_prefixed_string_encoder(request.player)

    @staticmethod
    def decode(payload):
        add = unpack_from('>B', payload) == 0
        payload = payload[calcsize('>B'):]
        player, payload = varint_prefixed_string_parser(payload)
        return RequestNotifyPlayer(add, player)
