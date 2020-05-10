from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec


class RequestAsServer(AbstractRequest):
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port


class RequestAsServerCodec(AbstractRequestCodec[RequestAsServer]):
    @staticmethod
    def encode(request: RequestAsServer) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestAsServer:
        ...
