from AbstractResult import AbstractResult, AbstractResultCodec


class ResultNotifyPlayer(AbstractResult):
    opcode = 0x21

    def __init__(self):
        pass


class ResultNotifyPlayerCodec(AbstractResultCodec):
    @staticmethod
    def encode(packet):
        return ''

    @staticmethod
    def decode(payload):
        return ResultNotifyPlayer()