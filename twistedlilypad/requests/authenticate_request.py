from .abstract_request import AbstractRequest, AbstractRequestCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser


class RequestAuthenticate(AbstractRequest):
    opcode = 0x00

    def __init__(self, username, password):
        self.username = username
        self.password = password


class RequestAuthenticateCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        assert isinstance(request, RequestAuthenticate)

        return varint_prefixed_string_encoder(request.username) + varint_prefixed_string_encoder(request.password)

    @staticmethod
    def decode(payload):
        username, payload = varint_prefixed_string_parser(payload)
        password, payload = varint_prefixed_string_parser(payload)
        return RequestAuthenticate(username, password)
