from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec


class RequestGetSalt(AbstractRequest):
    opcode = 0x03

    def __init__(self):
        pass


class RequestGetSaltCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request: RequestGetSalt) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestGetSalt:
        ...

