from AbstractResult import AbstractResult, AbstractResultCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


class ResultGetWhoAmI(AbstractResult):
    opcode = 0x04

    def __init__(self, whoAmI):
        self.whoAmI = whoAmI


class ResultGetWhoAmICodec(AbstractResultCodec):
    @staticmethod
    def encode(result):
        assert isinstance(result, ResultGetWhoAmI)

        return varIntPrefixedStringEncoder(result.whoAmI)

    @staticmethod
    def decode(payload):
        whoAmI, payload = varIntPrefixedStringParser(payload)

        return ResultGetWhoAmI(whoAmI)