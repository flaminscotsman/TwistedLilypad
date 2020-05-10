from struct import unpack_from, calcsize

from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec
from twistedlilypad.utilities import boolean_encoder


class RequestGetPlayers(AbstractRequest):
    opcode = 0x20

    def __init__(self, list_players, include_uuids=False):
        self.list_players = list_players
        self.include_uuids = include_uuids


class RequestGetPlayersCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        if request.include_uuids is None:
            return boolean_encoder(request.list_players)
        else:
            return boolean_encoder(request.list_players) + boolean_encoder(request.include_uuids)

    @staticmethod
    def decode(payload):
        list_players = unpack_from('>B', payload)[0] == 0

        if len(payload) > calcsize('>B'):
            include_uuids = unpack_from('>B', payload)[0] == 0
        else:
            include_uuids = False

        return RequestGetPlayers(list_players, include_uuids)
