from .abstract_result import AbstractResult, AbstractResultCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser


class ResultGetSalt(AbstractResult):
    opcode = 0x03

    def __init__(self, salt):
        self.salt = salt


class ResultGetSaltCodec(AbstractResultCodec):
    @staticmethod
    def encode(result):
        return varint_prefixed_string_encoder(result.salt)

    @staticmethod
    def decode(payload):
        salt, payload = varint_prefixed_string_parser(payload)

        return ResultGetSalt(salt)
