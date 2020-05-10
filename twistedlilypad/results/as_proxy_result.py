from .abstract_result import AbstractResult, AbstractResultCodec


class ResultAsProxy(AbstractResult):
    opcode = 0x02

    def __init__(self):
        pass


class ResultAsProxyCodec(AbstractResultCodec):
    @staticmethod
    def encode(packet):
        return b''

    @staticmethod
    def decode(payload):
        return ResultAsProxy()
