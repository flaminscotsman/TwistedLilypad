from .decoder_utilities import varint_parser, varint_parser_with_length, varint_prefixed_string_parser
from .encoder_utilities import varint_encoder, varint_prefixed_string_encoder, varint_prefixed_string_list_encoder, boolean_encoder
from .packet_utilties import make_packet_stream


def salt_password(password, salt):
    from hashlib import sha1

    content = sha1(salt.encode('utf-8')).hexdigest() + sha1(password.encode('utf-8')).hexdigest()
    return sha1(content.encode('utf-8')).hexdigest()
