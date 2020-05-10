from .abstract_request import AbstractRequest, AbstractRequestCodec


class RequestAuthenticate(AbstractRequest):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class RequestAuthenticateCodec(AbstractRequestCodec[RequestAuthenticate]):
    @staticmethod
    def encode(request: RequestAuthenticate) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestAuthenticate:
        ...

