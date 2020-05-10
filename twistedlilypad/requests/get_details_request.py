from .abstract_request import AbstractRequest, AbstractRequestCodec


class RequestGetDetails(AbstractRequest):
    opcode = 0x22

    def __init__(self):
        pass


class RequestGetDetailsCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        return b''

    @staticmethod
    def decode(payload):
        return RequestGetDetails()
