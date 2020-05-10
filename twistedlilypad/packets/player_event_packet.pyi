from uuid import UUID

from .abstract_packet import AbstractPacket, AbstractPacketCodec


class PacketPlayerEvent(AbstractPacket):
    def __init__(self, joining: bool, player_name: str, player_uuid: UUID):
        self.joining = joining
        self.player_name = player_name
        self.player_uuid = player_uuid


class PacketPlayerEventCodec(AbstractPacketCodec[PacketPlayerEvent]):
    ...
