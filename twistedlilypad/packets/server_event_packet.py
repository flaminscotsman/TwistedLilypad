from struct import unpack_from, calcsize, pack

from twistedlilypad.packets.abstract_packet import AbstractPacket, AbstractPacketCodec
from twistedlilypad.utilities import boolean_encoder, varint_prefixed_string_encoder, varint_prefixed_string_parser


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

        result = boolean_encoder(packet.add) + varint_prefixed_string_encoder(packet.server)
        if packet.add:
            return result + varint_prefixed_string_encoder(packet.securityKey) + \
                   varint_prefixed_string_encoder(packet.address) + pack('>H', packet.port)
        return result

    @staticmethod
    def decode(payload):
        add = unpack_from('>B', payload)[0] == 1
        payload = payload[calcsize('>B'):]
        server, payload = varint_prefixed_string_parser(payload)

        if add:
            securityKey, payload = varint_prefixed_string_parser(payload)
            address, payload = varint_prefixed_string_parser(payload)
            port = unpack_from('>H', payload)[0]

            return PacketServerEvent(add, server, securityKey, address, port)

        return PacketServerEvent(add, server)
