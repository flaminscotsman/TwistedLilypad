from .abstract_packet import AbstractPacket, AbstractPacketCodec


class PacketKeepAlive(AbstractPacket):
    def __init__(self, random: int):
        self.random = random


class PacketKeepAliveCodec(AbstractPacketCodec[PacketKeepAlive]):
    ...
