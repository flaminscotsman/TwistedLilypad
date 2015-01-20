from AbstractResult import AbstractResult, AbstractResultCodec


class ResultAuthenticate(AbstractResult):
    opcode = 0x00

    def __init__(self):
        pass


class ResultAuthenticateCodec(AbstractResultCodec):
    @staticmethod
    def encode(packet):
        return ''

    @staticmethod
    def decode(payload):
        return ResultAuthenticate()