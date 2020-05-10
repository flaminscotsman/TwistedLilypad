from struct import unpack_from, pack

from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser


class RequestAsServer(AbstractRequest):
    opcode = 0x01

    def __init__(self, address, port):
        self.address = address
        self.port = port


class RequestAsServerCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        return varint_prefixed_string_encoder(request.address) + pack('>H', request.port)

    @staticmethod
    def decode(payload):
        address, payload = varint_prefixed_string_parser(payload)
        port = unpack_from('>H', payload)
        return RequestAsServer(address, port[0])
