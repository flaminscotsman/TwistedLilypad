from .abstract_packet import AbstractPacket, AbstractPacketCodec


class PacketMessageEvent(AbstractPacket):
    def __init__(self, sender: str, channel: str, payload: bytes):
        self.sender = sender
        self.channel = channel
        self.payload = payload

    @property
    def payloadSize(self) -> int:
        ...

    @property
    def message(self) -> str:
        ...

    @message.setter
    def message(self, message: str):
        ...


class PacketMessageEventCodec(AbstractPacketCodec[PacketMessageEvent]):
    ...
