from twistedlilypad.Packets import codecLookup
from twistedlilypad.Packets.AbstractPacket import AbstractPacket
from twistedlilypad.Utilities.EncoderUtilities import varIntEncoder


def makePacketStream(packet):
    assert isinstance(packet, AbstractPacket)

    encodedPacket = codecLookup[packet.opcode].encode(packet)
    opcode = varIntEncoder(packet.opcode)
    return varIntEncoder(len(encodedPacket) + len(opcode)) + opcode + encodedPacket