from struct import calcsize, unpack_from, pack

from .abstract_result import AbstractResult, AbstractResultCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser


class ResultGetDetails(AbstractResult):
    opcode = 0x22

    def __init__(self, ip, port, motd, version):
        self.ip = ip
        self.port = port
        self.motd = motd
        self.version = version


class ResultGetDetailsCodec(AbstractResultCodec):
    @staticmethod
    def encode(result):
        return varint_prefixed_string_encoder(result.ip) + \
               pack('>H', result.port) + \
               varint_prefixed_string_encoder(result.motd) + \
               varint_prefixed_string_encoder(result.version)

    @staticmethod
    def decode(payload):
        ip, payload = varint_prefixed_string_parser(payload)

        port = unpack_from('>H', payload)
        payload = payload[calcsize('>H'):]

        motd, payload = varint_prefixed_string_parser(payload)
        version, payload = varint_prefixed_string_parser(payload)

        return ResultGetDetails(ip, port[0], motd, version)
