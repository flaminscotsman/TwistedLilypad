from struct import unpack_from, calcsize
from uuid import UUID

from .abstract_packet import AbstractPacket, AbstractPacketCodec
from twistedlilypad.utilities import boolean_encoder, varint_prefixed_string_encoder, varint_prefixed_string_parser


class PacketPlayerEvent(AbstractPacket):
    opcode = 0x06

    def __init__(self, joining, player_name, player_uuid):
        self.joining = joining
        self.player_name = player_name
        self.player_uuid = player_uuid

    def __eq__(self, other):
        if not isinstance(other, PacketPlayerEvent):
            return NotImplemented
        return self.server == other.server and \
            self.player == other.player


class PacketPlayerEventCodec(AbstractPacketCodec):
    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketPlayerEvent)

        return boolean_encoder(packet.joining) + varint_prefixed_string_encoder(packet.player_name) + packet.player_uuid.bytes

    @staticmethod
    def decode(payload):
        joining = unpack_from('>B', payload)[0]
        payload = payload[calcsize('>B'):]

        player_name, payload = varint_prefixed_string_parser(payload)
        player_uuid = UUID(bytes=payload[:32])

        return PacketPlayerEvent(joining, player_name, player_uuid)
