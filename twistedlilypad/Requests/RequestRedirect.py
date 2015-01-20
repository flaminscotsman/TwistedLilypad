from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


class RequestRedirect(AbstractRequest):
    opcode = 0x11

    def __init__(self, server, player):
        self.server = server
        self.player = player


class RequestRedirectCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestRedirect)

        return varIntPrefixedStringEncoder(request.server) + varIntPrefixedStringEncoder(request.player)

    @staticmethod
    def decode(payload):
        server, payload = varIntPrefixedStringParser(payload)
        player, payload = varIntPrefixedStringParser(payload)
        return RequestRedirect(server, player)