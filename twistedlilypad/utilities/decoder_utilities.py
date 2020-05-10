def varint_parser(data):
    return varint_parser_with_length(data)[:2]


def varint_parser_with_length(data):
    value = 0
    shift = 0
    byte = data[shift]
    if not isinstance(byte, int):
        byte = ord(byte)

    while True:
        value |= (byte & 0x7F) << (shift * 7)
        shift += 1

        if shift > 5:
            raise OverflowError("VarInt is too long")

        if byte & 0x80 == 0:
            break

        byte = data[shift]
        if not isinstance(byte, int):
            byte = ord(byte)

    return value, data[shift:], shift


def varint_prefixed_string_parser(data):
    length, data = varint_parser(data)

    return data[:length].decode('utf-8'), data[length:]
