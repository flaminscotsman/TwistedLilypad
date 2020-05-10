from .abstract_request import AbstractRequest, AbstractRequestCodec


class RequestNotifyPlayer(AbstractRequest):
    def __init__(self, joining: bool, player: str):
        self.joining = joining
        self.player = player


class RequestNotifyPlayerCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request: RequestNotifyPlayer) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestNotifyPlayer:
        ...
