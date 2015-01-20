from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec


class RequestGetSalt(AbstractRequest):
    opcode = 0x03

    def __init__(self):
        pass


class RequestGetSaltCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestGetSalt)

        return ''

    @staticmethod
    def decode(payload):
        return RequestGetSalt()