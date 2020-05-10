from .abstract_request import AbstractRequest, AbstractRequestCodec


class RequestAsProxy(AbstractRequest):
    def __init__(self, address: str, port: int, motd: str, version: str, max_players: str):
        self.address = address
        self.port = port
        self.motd = motd
        self.version = version
        self.max_players = max_players


class RequestAsProxyCodec(AbstractRequestCodec[RequestAsProxy]):
    @staticmethod
    def decode(payload: bytes) -> RequestAsProxy:
        ...

    @staticmethod
    def encode(request: RequestAsProxy) -> bytes:
        ...
