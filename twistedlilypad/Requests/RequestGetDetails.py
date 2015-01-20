from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec


class RequestGetDetails(AbstractRequest):
    opcode = 0x22

    def __init__(self):
        pass


class RequestGetDetailsCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestGetDetails)

        return ''

    @staticmethod
    def decode(payload):
        return RequestGetDetails()