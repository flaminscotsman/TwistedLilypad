from AbstractResult import AbstractResult, AbstractResultCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


class ResultGetSalt(AbstractResult):
    opcode = 0x03

    def __init__(self, salt):
        self.salt = salt


class ResultGetSaltCodec(AbstractResultCodec):
    @staticmethod
    def encode(result):
        assert isinstance(result, ResultGetSalt)

        return varIntPrefixedStringEncoder(result.salt)

    @staticmethod
    def decode(payload):
        salt, payload = varIntPrefixedStringParser(payload)

        return ResultGetSalt(salt)