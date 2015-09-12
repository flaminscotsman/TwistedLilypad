from struct import unpack_from, calcsize, pack

from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec, StatusCode


class PacketResult(AbstractPacket):
    opcode = 0x02

    def __init__(self, sequenceID, statusCode, payload=None):
        self.sequenceID = sequenceID
        self.statusCode = statusCode
        self.payload = payload

    @property
    def payloadSize(self):
        return len(self.payload)

    def __eq__(self, other):
        if not isinstance(other, PacketResult):
            return NotImplemented
        return self.sequenceID == other.sequenceID and \
            self.statusCode == other.statusCode and \
            self.payload == other.payload


class PacketResultCodec(AbstractPacketCodec):
    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketResult)

        if packet.statusCode == StatusCode.SUCCESS:
            return pack('>iBH', packet.sequenceID, packet.statusCode, packet.payloadSize) + packet.payload
        return pack('>iB', packet.sequenceID, packet.statusCode)

    @staticmethod
    def decode(payload):
        sequenceID, statusCode = unpack_from('>iB', payload)
        payload = payload[calcsize('>iB'):]

        if statusCode == StatusCode.SUCCESS:
            payloadSize = unpack_from('>H', payload)[0]
            payload = payload[calcsize('>H'):]
            return PacketResult(sequenceID, statusCode, payload)

        return PacketResult(sequenceID, statusCode)