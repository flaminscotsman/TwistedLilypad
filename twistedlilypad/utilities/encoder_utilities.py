from struct import pack


def varint_encoder(number):
    result = []
    while number >= 0x80:
        result.append((number & 0x7F) | 0x80)
        number >>= 7

    result.append(number)

    return pack('>' + 'B' * len(result), *result)


def varint_prefixed_string_encoder(string):
    encoded = string.encode('utf-8')
    return varint_encoder(len(encoded)) + encoded


def varint_prefixed_string_list_encoder(string_list):
    return b''.join(map(varint_prefixed_string_encoder, string_list))


def boolean_encoder(boolean):
    return pack('>B', 1 if boolean else 0)
