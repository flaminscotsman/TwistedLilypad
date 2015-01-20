from struct import unpack_from

from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder


class RequestGetPlayers(AbstractRequest):
    opcode = 0x20

    def __init__(self, listPlayers):
        self.listPlayers = listPlayers


class RequestGetPlayersCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestGetPlayers)

        return booleanEncoder(request.listPlayers)

    @staticmethod
    def decode(payload):
        listPlayers = unpack_from('>B', payload)[0] == 0

        return RequestGetPlayers(listPlayers)