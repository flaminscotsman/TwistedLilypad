from AbstractResult import AbstractResult, AbstractResultCodec


class ResultRedirect(AbstractResult):
    opcode = 0x11

    def __init__(self, server, player):
        pass


class ResultRedirectCodec(AbstractResultCodec):
    @staticmethod
    def encode(packet):
        return ''

    @staticmethod
    def decode(payload):
        return ResultRedirect()