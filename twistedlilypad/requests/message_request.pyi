from .abstract_request import AbstractRequest, AbstractRequestCodec

class RequestMessage(AbstractRequest):
    opcode = 0x10

    def __init__(self, recipients, channel, message):
        self.recipients = recipients
        self.channel = channel
        self.message = message


class RequestMessageCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request: RequestMessage) -> bytes:
        ...

    @staticmethod
    def decode(payload: bytes) -> RequestMessage:
        ...
