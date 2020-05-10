from typing import Dict, Iterable, Optional
from uuid import UUID

from .abstract_result import AbstractResult, AbstractResultCodec


class ResultGetPlayers(AbstractResult):
    def __init__(self, list_players: bool, current_players: int, max_players: int,
                 players: Optional[Iterable[str]]=None, include_uuids: Optional[bool]=None, uuids: Optional[str]=None):
        self.listPlayers = list_players
        self.includeUUIDs = include_uuids
        self.currentPlayers = current_players
        self.maxPlayers = max_players
        self.players = players
        self.uuids = uuids

        self.playersToUUID: Optional[Dict[str, UUID]]


class ResultGetPlayersCodec(AbstractResultCodec[ResultGetPlayers]):
    ...
