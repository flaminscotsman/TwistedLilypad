from .abstract_packet import AbstractPacket, AbstractPacketCodec
from twistedlilypad.utilities import varint_prefixed_string_parser, varint_prefixed_string_encoder

class PacketRedirectEvent(AbstractPacket):
    opcode = 0x04

    def __init__(self, server, player):
        self.server = server
        self.player = player

    def __eq__(self, other):
        if not isinstance(other, PacketRedirectEvent):
            return NotImplemented
        return self.server == other.server and \
            self.player == other.player


class PacketRedirectEventCodec(AbstractPacketCodec):
    @staticmethod
    def encode(packet):
        return varint_prefixed_string_encoder(packet.server) + varint_prefixed_string_encoder(packet.player)

    @staticmethod
    def decode(payload):
        server, payload = varint_prefixed_string_parser(payload)
        player, payload = varint_prefixed_string_parser(payload)
        return PacketRedirectEvent(server, player)
