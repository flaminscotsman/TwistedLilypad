from typing import Optional

from .abstract_packet import AbstractPacket, AbstractPacketCodec


class PacketServerEvent(AbstractPacket):
    def __init__(self, add, server, securityKey=None, address=None, port=None):
        self.add = add
        self.server = server
        self.securityKey = securityKey
        self.address = address
        self.port = port


class PacketServerEventCodec(AbstractPacketCodec[PacketServerEvent]):
    ...
