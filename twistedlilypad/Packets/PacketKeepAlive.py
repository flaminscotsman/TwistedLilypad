from struct import unpack_from, pack

from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec


class PacketKeepAlive(AbstractPacket):
    opcode = 0x00

    def __init__(self, random):
        self.random = random


class PacketKeepAliveCodec(AbstractPacketCodec):
    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketKeepAlive)
        return pack('>i', packet.random)

    @staticmethod
    def decode(payload):
        random = unpack_from('>i', payload)[0]
        return PacketKeepAlive(random)