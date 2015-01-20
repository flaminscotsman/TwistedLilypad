from twisted.internet import defer
from twisted.internet.protocol import Protocol

from twistedlilypad.Packets import AbstractPacket, codecLookup as packetCodecLookup, PacketRequest, PacketResult, StatusCode
from twistedlilypad.Requests import codecLookup as requestCodecLookup
from twistedlilypad.Requests.AbstractRequest import AbstractRequest
from twistedlilypad.Results import codecLookup as resultCodecLookup
from twistedlilypad.Utilities.DecoderUtilities import varIntParser, varIntParserWithLength
from twistedlilypad.Utilities.PacketUtilties import makePacketStream


class ParserState(object):
    WAITING, READING_PACKET_OPCODE, READING_PACKET_PAYLOAD = range(3)


class LilypadProtocol(object, Protocol):
    _buffer = ''
    _state = ParserState.WAITING

    _payloadSize = 0
    _opcode = 0
    _payload = ''

    def dataReceived(self, data):
        self._buffer += data

        if self._state == ParserState.WAITING:
            try:
                self._payloadSize, self._buffer = varIntParser(self._buffer)
                self._state = ParserState.READING_PACKET_OPCODE
            except IndexError:
                return  # Just means there wasn't enough data to parse the varint

        if self._state == ParserState.READING_PACKET_OPCODE:
            try:
                self._opcode, self._buffer, opcodeLength = varIntParserWithLength(self._buffer)
                self._payloadSize -= opcodeLength
                self._state = ParserState.READING_PACKET_PAYLOAD
            except IndexError:
                return  # Just means there wasn't enough data to parse the varint

        if self._state == ParserState.READING_PACKET_PAYLOAD:
            if len(self._buffer) >= self._payloadSize:
                self._payload = self._buffer[:self._payloadSize]
                self._buffer = self._buffer[self._payloadSize:]
                self._state = ParserState.WAITING

                self.rawPacketReceived(self._opcode, self._payload)

                packet = packetCodecLookup[self._opcode].decode(self._payload)
                self.packetReceived(packet)

    def rawPacketReceived(self, opcode, packetData):
        pass

    def packetReceived(self, packet):
        pass

    def writePacket(self, packet):
        self.transport.write(makePacketStream(packet))

    def onKeepAlivePacket(self, KeepAlivePacket):
        self.writePacket(KeepAlivePacket)

    def onRequestPacket(self, RequestPacket):
        pass

    def onResultPacket(self, ResultPacket):
        pass

    def onMessageEventPacket(self, MessageEventPacket):
        pass

    def onRedirectEventPacket(self, RedirectEventPacket):
        pass

    def onServerEventPacket(self, ServerEventPacket):
        pass

    def _packetDirector(self, packet):
        assert isinstance(packet, AbstractPacket)

        if packet.opcode == 0x00:
            self.onKeepAlivePacket(packet)
        elif packet.opcode == 0x01:
            self.onRequestPacket(packet)
        elif packet.opcode == 0x02:
            self.onResultPacket(packet)
        elif packet.opcode == 0x03:
            self.onMessageEventPacket(packet)
        elif packet.opcode == 0x04:
            self.onRedirectEventPacket(packet)
        elif packet.opcode == 0x05:
            self.onServerEventPacket(packet)
        else:
            raise RuntimeWarning("Unknown packet received")


class LilypadClientProtocol(LilypadProtocol):
    sequenceID = 0
    currentRequests = {}

    def writeRequest(self, request):
        assert isinstance(request, AbstractRequest)

        deferred = defer.Deferred()
        packet = PacketRequest(self.sequenceID, request.opcode, requestCodecLookup[request.opcode].encode(request))

        self.currentRequests[self.sequenceID] = (deferred, resultCodecLookup[request.opcode])
        self.sequenceID += 1
        self.writePacket(packet)

        return deferred

    def _packetDirector(self, packet):
        assert isinstance(packet, AbstractPacket)

        if packet.opcode == 0x00:
            self.onKeepAlivePacket(packet)
        elif packet.opcode == 0x01:
            self.onRequestPacket(packet)
        elif packet.opcode == 0x02:
            self._resultCallbackHandler(packet)
            self.onResultPacket(packet)
        elif packet.opcode == 0x03:
            self.onMessageEventPacket(packet)
        elif packet.opcode == 0x04:
            self.onRedirectEventPacket(packet)
        elif packet.opcode == 0x05:
            self.onServerEventPacket(packet)
        else:
            raise RuntimeWarning("Unknown packet received")

    def _resultCallbackHandler(self, resultPacket):
        assert isinstance(resultPacket, PacketResult)
        assert resultPacket.sequenceID in self.currentRequests

        deferred, codec = self.currentRequests.pop(resultPacket.sequenceID)
        if resultPacket.statusCode != StatusCode.SUCCESS:
            deferred.errback(resultPacket.statusCode)
            return
        deferred.callback(codec.decode(resultPacket.payload))