from codecs import getdecoder, getencoder
from struct import unpack_from, calcsize, pack

from twistedlilypad.Requests.AbstractRequest import AbstractRequest, AbstractRequestCodec
from twistedlilypad.Utilities.DecoderUtilities import varIntPrefixedStringParser
from twistedlilypad.Utilities.EncoderUtilities import varIntPrefixedStringEncoder, varIntPrefixedStringListEncoder


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
        assert isinstance(request, RequestMessage)

        encoded_message = uft8_encoder(request.message)[0]
        return pack('>H', len(request.recipients)) + \
               varIntPrefixedStringListEncoder(request.recipients) + \
               varIntPrefixedStringEncoder(request.channel) + \
               pack('>H', len(encoded_message)) + \
               encoded_message

    @staticmethod
    def decode(payload):
        recipientsSize = unpack_from('>H', payload)[0]
        payload = payload[calcsize('>H'):]

        recipients = []
        for i in xrange(recipientsSize):
            recipient, payload = varIntPrefixedStringParser(payload)
            recipients.append(recipient)

        channel, payload = varIntPrefixedStringParser(payload)

        messageSize = unpack_from('>H', payload)[0]
        payload = payload[calcsize('>H'):]

        message = uft8_decoder(payload[:messageSize])[0]

        return RequestMessage(recipients, channel, message)