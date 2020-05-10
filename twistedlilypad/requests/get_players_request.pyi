from .abstract_request import AbstractRequest, AbstractRequestCodec


class RequestGetPlayers(AbstractRequest):
    def __init__(self, list_players: bool, include_uuids: bool = False):
        self.list_players = list_players
        self.include_uuids = include_uuids


class RequestGetPlayersCodec(AbstractRequestCodec[RequestGetPlayers]):
    @staticmethod
    def encode(request: RequestGetPlayers) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestGetPlayers:
        ...

