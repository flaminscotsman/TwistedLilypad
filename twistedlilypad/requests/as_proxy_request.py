from struct import unpack_from, calcsize, pack

from .abstract_request import AbstractRequest, AbstractRequestCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser


class RequestAsProxy(AbstractRequest):
    opcode = 0x02

    def __init__(self, address, port, motd, version, max_players):
        self.address = address
        self.port = port
        self.motd = motd
        self.version = version
        self.max_players = max_players


class RequestAsProxyCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        return varint_prefixed_string_encoder(request.address) + \
               pack('>H', request.port) + \
               varint_prefixed_string_parser(request.motd) + \
               varint_prefixed_string_encoder(request.version) + \
               pack('>H', request.max_players)

    @staticmethod
    def decode(payload):
        address, payload = varint_prefixed_string_parser(payload)

        port = unpack_from('>H', payload)[0]
        payload = payload[calcsize('>H'):]

        motd, payload = varint_prefixed_string_parser(payload)
        version, payload = varint_prefixed_string_parser(payload)

        maxPlayers = unpack_from('>H', payload)[0]

        return RequestAsProxy(address, port, motd, version, maxPlayers)
