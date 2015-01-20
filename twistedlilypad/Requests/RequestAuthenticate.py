from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


class RequestAuthenticate(AbstractRequest):
    opcode = 0x00

    def __init__(self, username, password):
        self.username = username
        self.password = password


class RequestAuthenticateCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestAuthenticate)

        return varIntPrefixedStringEncoder(request.username) + varIntPrefixedStringEncoder(request.password)

    @staticmethod
    def decode(payload):
        username, payload = varIntPrefixedStringParser(payload)
        password, payload = varIntPrefixedStringParser(payload)
        return RequestAuthenticate(username, password)