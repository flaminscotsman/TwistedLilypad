from .abstract_result import AbstractResult, AbstractResultCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser


class ResultGetWhoAmI(AbstractResult):
    opcode = 0x04

    def __init__(self, whoAmI):
        self.identifier = whoAmI


class ResultGetWhoAmICodec(AbstractResultCodec):
    @staticmethod
    def encode(result):
        return varint_prefixed_string_encoder(result.identifier)

    @staticmethod
    def decode(payload):
        identifier, payload = varint_prefixed_string_parser(payload)

        return ResultGetWhoAmI(identifier)
