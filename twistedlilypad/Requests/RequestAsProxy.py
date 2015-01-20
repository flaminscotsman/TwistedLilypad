from struct import unpack_from, calcsize, pack

from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


class RequestAsProxy(AbstractRequest):
    opcode = 0x02

    def __init__(self, address, port, motd, version, maxPlayers):
        self.address = address
        self.port = port
        self.motd = motd
        self.version = version
        self.maxPlayers = maxPlayers


class RequestAsProxyCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestAsProxy)

        return varIntPrefixedStringEncoder(request.address) + \
               pack('>H', request.port) + \
               varIntPrefixedStringEncoder(request.motd) + \
               varIntPrefixedStringEncoder(request.version) + \
               pack('>H', request.maxPlayers)

    @staticmethod
    def decode(payload):
        address, payload = varIntPrefixedStringParser(payload)

        port = unpack_from('>H', payload)
        payload = payload[calcsize('>H'):]

        motd, payload = varIntPrefixedStringParser(payload)
        version, payload = varIntPrefixedStringParser(payload)

        maxPlayers = unpack_from('>H', payload)

        return RequestAsProxy(address, port, motd, version, maxPlayers)