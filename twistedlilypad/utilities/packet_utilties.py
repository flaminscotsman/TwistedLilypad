from .encoder_utilities import varint_encoder


def make_packet_stream(packet):
    from twistedlilypad.packets import codecLookup

    opcode = varint_encoder(packet.opcode)
    encoded_packet = codecLookup[packet.opcode].encode(packet)
    return varint_encoder(len(opcode) + len(encoded_packet)) + opcode + encoded_packet
