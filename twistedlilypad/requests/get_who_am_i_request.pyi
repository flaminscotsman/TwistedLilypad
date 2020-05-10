from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec


class RequestGetWhoAmI(AbstractRequest):
    opcode = 0x04

    def __init__(self):
        pass


class RequestGetWhoAmICodec(AbstractRequestCodec):
    @staticmethod
    def encode(request: RequestGetWhoAmI) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestGetWhoAmI:
        ...
