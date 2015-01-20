from codecs import getdecoder
from struct import unpack


uft8_decoder = getdecoder('UTF-8')


def varIntParser(data):
    return varIntParserWithLength(data)[:2]


def varIntParserWithLength(data):
    value = 0
    shift = 0
    byte = unpack('!B', data[shift])[0]

    while True:
        value |= (byte & 0x7F) << (shift * 7)
        shift += 1

        if shift > 5:
            raise OverflowError("VarInt is too long")

        if byte & 0x80 == 0:
            break

        byte = unpack('!B', data[shift])[0]

    return value, data[shift:], shift


def varIntPrefixedStringParser(data):
    length, data = varIntParser(data)

    value = uft8_decoder(data[:length])[0]  # codec.decode returns a 2-tuple of (output, length consumed)

    return value, data[length:]