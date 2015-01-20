from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec


class RequestGetWhoAmI(AbstractRequest):
    opcode = 0x04

    def __init__(self):
        pass


class RequestGetWhoAmICodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestGetWhoAmI)

        return ''

    @staticmethod
    def decode(payload):
        return RequestGetWhoAmI()