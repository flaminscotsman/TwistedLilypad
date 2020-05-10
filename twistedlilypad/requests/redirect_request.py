from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser


class RequestRedirect(AbstractRequest):
    opcode = 0x11

    def __init__(self, server, player):
        self.server = server
        self.player = player


class RequestRedirectCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        return varint_prefixed_string_encoder(request.server) + varint_prefixed_string_encoder(request.player)

    @staticmethod
    def decode(payload):
        server, payload = varint_prefixed_string_parser(payload)
        player, payload = varint_prefixed_string_parser(payload)
        return RequestRedirect(server, player)
