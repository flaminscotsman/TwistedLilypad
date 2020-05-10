from .abstract_request import AbstractRequest, AbstractRequestCodec


class RequestRedirect(AbstractRequest):
    def __init__(self, server: str, player: str):
        self.server = server
        self.player = player


class RequestRedirectCodec(AbstractRequestCodec[RequestRedirect]):
    @staticmethod
    def encode(request: RequestRedirect) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestRedirect:
        ...
