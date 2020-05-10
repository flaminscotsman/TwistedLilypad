from .abstract_packet import AbstractPacket, AbstractPacketCodec


class PacketRequest(AbstractPacket):
    def __init__(self, sequence_id: int, request_id: int, payload: bytes):
        self.sequenceID = sequence_id
        self.requestID = request_id
        self.payload = payload

    @property
    def payloadSize(self) -> int:
        ...


class PacketRequestCodec(AbstractPacketCodec[PacketRequest]):
    ...
