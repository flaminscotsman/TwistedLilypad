from codecs import getdecoder, getencoder
from struct import unpack_from, calcsize, pack

from six.moves import xrange

from twistedlilypad.requests.abstract_request import AbstractRequest, AbstractRequestCodec
from twistedlilypad.utilities import varint_prefixed_string_encoder, varint_prefixed_string_parser, varint_prefixed_string_list_encoder


uft8_decoder = getdecoder('UTF_8')
uft8_encoder = getencoder('UTF_8')


class RequestMessage(AbstractRequest):
    opcode = 0x10

    def __init__(self, recipients, channel, message):
        self.recipients = recipients
        self.channel = channel
        self.message = message


class RequestMessageCodec(AbstractRequestCodec):
    @staticmethod
    def encode(request):
        encoded_message = uft8_encoder(request.message)[0]
        return pack('>H', len(request.recipients)) + \
            varint_prefixed_string_list_encoder(request.recipients) + \
            varint_prefixed_string_encoder(request.channel) + \
            pack('>H', len(encoded_message)) + \
            encoded_message

    @staticmethod
    def decode(payload):
        recipientsSize = unpack_from('>H', payload)[0]
        payload = payload[calcsize('>H'):]

        recipients = []
        for _ in xrange(recipientsSize):
            recipient, payload = varint_prefixed_string_encoder(payload)
            recipients.append(recipient)

        channel, payload = varint_prefixed_string_parser(payload)

        message_size = unpack_from('>H', payload)[0]
        payload = payload[calcsize('>H'):]

        message = uft8_decoder(payload[:message_size])[0]

        return RequestMessage(recipients, channel, message)
