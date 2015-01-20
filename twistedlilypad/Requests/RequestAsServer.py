from struct import unpack_from, pack

from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


class RequestAsServer(AbstractRequest):
    opcode = 0x01

    def __init__(self, address, port):
        self.address = address
        self.port = port


class RequestAsServerCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestAsServer)

        return varIntPrefixedStringEncoder(request.address) + pack('>H', request.port)

    @staticmethod
    def decode(payload):
        address, payload = varIntPrefixedStringParser(payload)
        port = unpack_from('>H', payload)
        return RequestAsServer(address, port)