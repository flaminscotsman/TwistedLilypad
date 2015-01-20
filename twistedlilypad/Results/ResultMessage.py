from AbstractResult import AbstractResult, AbstractResultCodec


class ResultMessage(AbstractResult):
    opcode = 0x10

    def __init__(self):
        pass


class ResultMessageCodec(AbstractResultCodec):
    @staticmethod
    def encode(packet):
        return ''

    @staticmethod
    def decode(payload):
        return ResultMessage()