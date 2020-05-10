from .abstract_result import AbstractResult, AbstractResultCodec


class ResultAsServer(AbstractResult):
    opcode = 0x01

    def __init__(self):
        pass


class ResultAsServerCodec(AbstractResultCodec):
    @staticmethod
    def encode(packet):
        return b''

    @staticmethod
    def decode(payload):
        return ResultAsServer()
