from struct import calcsize, unpack_from, pack

from AbstractResult import AbstractResult, AbstractResultCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder, varIntPrefixedStringListEncoder


class ResultGetPlayers(AbstractResult):
    opcode = 0x20

    def __init__(self, listPlayers, currentPlayers, maxPlayers, players=None):
        self.listPlayers = listPlayers
        self.currentPlayers = currentPlayers
        self.maxPlayers = maxPlayers
        self.players = players


class ResultGetPlayersCodec(AbstractResultCodec):
    @staticmethod
    def encode(result):
        assert isinstance(result, ResultGetPlayers)

        ret = booleanEncoder(result.listPlayers) + pack('>HH', result.currentPlayers, result.maxPlayers)
        if result.listPlayers:
            return ret + varIntPrefixedStringListEncoder(result.players)
        return ret

    @staticmethod
    def decode(payload):
        listPlayers, currentPlayers, maxPlayers = unpack_from('>BHH', payload)
        listPlayers = listPlayers != 0
        payload = payload[calcsize('>BHH'):]

        if listPlayers:
            players = []
            for i in xrange(currentPlayers):
                player, payload = varIntPrefixedStringParser(payload)
                players.append(player)

            return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers, players)

        return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers)