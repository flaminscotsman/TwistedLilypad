from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder


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
        assert isinstance(packet, PacketRedirectEvent)

        return varIntPrefixedStringEncoder(packet.server) + varIntPrefixedStringEncoder(packet.player)

    @staticmethod
    def decode(payload):
        server, payload = varIntPrefixedStringParser(payload)
        player, payload = varIntPrefixedStringParser(payload)
        return PacketRedirectEvent(server, player)