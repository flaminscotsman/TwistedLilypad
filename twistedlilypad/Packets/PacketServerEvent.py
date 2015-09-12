from struct import unpack_from, calcsize, pack

from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import booleanEncoder, varIntPrefixedStringEncoder


class PacketServerEvent(AbstractPacket):
    opcode = 0x05

    def __init__(self, add, server, securityKey=None, address=None, port=None):
        self.add = add
        self.server = server
        self.securityKey = securityKey
        self.address = address
        self.port = port

    def __eq__(self, other):
        if not isinstance(other, PacketServerEvent):
            return NotImplemented
        return self.add == other.add and \
            self.address == other.address and \
            self.port == other.port and \
            self.securityKey == other.securityKey and \
            self.server == other.server


class PacketServerEventCodec(AbstractPacketCodec):
    @staticmethod
    def encode(packet):
        assert isinstance(packet, PacketServerEvent)

        result = booleanEncoder(packet.add) + varIntPrefixedStringEncoder(packet.server)
        if packet.add:
            return result + varIntPrefixedStringEncoder(packet.securityKey) + \
                   varIntPrefixedStringEncoder(packet.address) + pack('>H', packet.port)
        return result

    @staticmethod
    def decode(payload):
        add = unpack_from('>B', payload)[0] == 1
        payload = payload[calcsize('>B'):]
        server, payload = varIntPrefixedStringParser(payload)

        if add:
            securityKey, payload = varIntPrefixedStringParser(payload)
            address, payload = varIntPrefixedStringParser(payload)
            port = unpack_from('>H', payload)[0]

            return PacketServerEvent(add, server, securityKey, address, port)

        return PacketServerEvent(add, server)