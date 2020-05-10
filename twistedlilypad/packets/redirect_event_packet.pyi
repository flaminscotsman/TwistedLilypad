from .abstract_packet import AbstractPacket, AbstractPacketCodec


class PacketRedirectEvent(AbstractPacket):
    def __init__(self, server: str, player: str):
        self.server = server
        self.player = player


class PacketRedirectEventCodec(AbstractPacketCodec[PacketRedirectEvent]):
    ...
