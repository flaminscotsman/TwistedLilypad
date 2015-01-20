from struct import calcsize, unpack_from

from AbstractResult import AbstractResult, AbstractResultCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


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
        assert isinstance(result, ResultGetDetails)

        return varIntPrefixedStringEncoder(result.address) + \
               pack('>H', result.port) + \
               varIntPrefixedStringEncoder(result.motd) + \
               varIntPrefixedStringEncoder(result.version)

    @staticmethod
    def decode(payload):
        ip, payload = varIntPrefixedStringParser(payload)

        port = unpack_from('>H', payload)
        payload = payload[calcsize('>H'):]

        motd, payload = varIntPrefixedStringParser(payload)
        version, payload = varIntPrefixedStringParser(payload)

        return ResultGetDetails(ip, port, motd, version)