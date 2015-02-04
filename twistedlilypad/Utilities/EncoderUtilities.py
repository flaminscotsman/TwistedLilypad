from codecs import getencoder
from struct import pack


uft8_encoder = getencoder('UTF_8')


def varIntEncoder(number):
    result = []
    while number >= 0x80:
        result.append(pack('>B', (number & 0x7F) | 0x80))
        number >>= 7

    result.append(pack('>B', number))

    return ''.join(result)


def varIntPrefixedStringEncoder(string):
    encoded_string = uft8_encoder(string)[0]
    return varIntEncoder(len(encoded_string)) + encoded_string


def varIntPrefixedStringListEncoder(string_list):
    return ''.join(varIntPrefixedStringEncoder(string) for string in string_list)


def booleanEncoder(boolean):
    return pack('>B', 1 if boolean else 0)