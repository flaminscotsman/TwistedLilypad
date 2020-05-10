from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec


class RequestGetWhoAmI(AbstractRequest):
    opcode = 0x04

    def __init__(self):
        pass


class RequestGetWhoAmICodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        return b''

    @staticmethod
    def decode(payload):
        return RequestGetWhoAmI()
