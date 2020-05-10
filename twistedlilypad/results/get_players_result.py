from struct import calcsize, unpack_from, pack
from uuid import UUID

from six.moves import xrange

from .abstract_result import AbstractResult, AbstractResultCodec
from twistedlilypad.utilities import boolean_encoder, varint_prefixed_string_list_encoder, varint_prefixed_string_parser

class ResultGetPlayers(AbstractResult):
    opcode = 0x20

    def __init__(self, listPlayers, currentPlayers, maxPlayers, players=None, includeUUIDs=None, uuids=None):
        self.listPlayers = listPlayers
        self.includeUUIDs = includeUUIDs
        self.currentPlayers = currentPlayers
        self.maxPlayers = maxPlayers
        self.players = players
        self.uuids = uuids

        if players is not None and uuids is not None:
            self.playersToUUID = dict(zip(players, uuids))
        else:
            self.playersToUUID = None


class ResultGetPlayersCodec(AbstractResultCodec):
    @staticmethod
    def encode(result):
        assert isinstance(result, ResultGetPlayers)

        ret = boolean_encoder(result.listPlayers) + pack('>HH', result.currentPlayers, result.maxPlayers)
        if result.listPlayers:
            return ret + varint_prefixed_string_list_encoder(result.players)

        if result.includeUUIDs is not None:
            ret += boolean_encoder(result.includeUUIDs)
            if result.includeUUIDs:
                for uuid in result.uuids:
                    ret += uuid.bytes

        return ret

    @staticmethod
    def decode(payload):
        listPlayers, currentPlayers, maxPlayers = unpack_from('>BHH', payload)
        listPlayers = listPlayers != 0
        payload = payload[calcsize('>BHH'):]

        if listPlayers:
            players = []
            for i in xrange(currentPlayers):
                player, payload = varint_prefixed_string_parser(payload)
                players.append(player)

            if not payload:
                return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers, players)

            def parse_uuid(payload):
                return UUID(bytes=payload[:16]), payload[16:]

            includeUUIDs = unpack_from('>B', payload)[0] != 0
            payload = payload[calcsize('>B'):]
            if includeUUIDs:
                uuids = []
                for i in xrange(currentPlayers):
                    uuid, payload = parse_uuid(payload)
                    uuids.append(uuid)

                return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers, players, includeUUIDs, uuids)

            return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers, players, includeUUIDs)

        return ResultGetPlayers(listPlayers, currentPlayers, maxPlayers)
