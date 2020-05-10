from typing import Optional

from .abstract_packet import AbstractPacket, AbstractPacketCodec


class PacketResult(AbstractPacket):
    def __init__(self, sequenceID: int, statusCode: int, payload: Optional[bytes] = None):
        self.sequenceID = sequenceID
        self.statusCode = statusCode
        self.payload = payload

    @property
    def payloadSize(self) -> int:
        ...


class PacketResultCodec(AbstractPacketCodec[PacketResult]):
    ...
