from twisted.internet import defer
from twisted.internet.protocol import Protocol

from twistedlilypad.Packets import AbstractPacket, codecLookup as packetCodecLookup, PacketRequest, PacketResult, StatusCode
from twistedlilypad.Requests import codecLookup as requestCodecLookup, RequestGetSalt, RequestAuthenticate
from twistedlilypad.Requests.AbstractRequest import AbstractRequest
from twistedlilypad.Results import codecLookup as resultCodecLookup
from twistedlilypad.Utilities import saltPassword
from twistedlilypad.Utilities.DecoderUtilities import varIntParser, varIntParserWithLength
from twistedlilypad.Utilities.PacketUtilties import makePacketStream


class ParserState(object):
    WAITING, READING_PACKET_OPCODE, READING_PACKET_PAYLOAD = range(3)


class LilypadProtocol(object, Protocol):
    """ Lilypad protocol implementation"""
    _buffer = ''
    _state = ParserState.WAITING

    _payloadSize = 0
    _opcode = 0
    _payload = ''

    def dataReceived(self, data):
        """Receives incoming data.

        Whenever a complete packet is received, this method extracts the payload and calls
        :py:meth:`~_packetDirector` forward it to the correct handler.
        :param data: A chunk of data representing a (possibly partial) lilypad packet
        :type data: basestring
        :rtype : None
        """
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

                self._packetDirector(packet)

    def rawPacketReceived(self, opcode, packetData):
        """Called when an unpacked lilypad packet is received.

        :param opcode: Opcode of received packet
        :type opcode: int
        :param packetData: Raw packed data of received packet
        :type opcode: basestring
        """
        pass

    def packetReceived(self, packet):
        """Called when a lilypad packet is received.

        :param packet: Parsed lilypad packet
        :type packet: AbstractPacket
        """
        pass

    def writePacket(self, packet):
        """Used to send an outgoing packet.

        :param packet: Outgoing packet
        :type packet: AbstractPacket
        """
        self.transport.write(makePacketStream(packet))

    def onKeepAlivePacket(self, KeepAlivePacket):
        """Called when a keep-alive packet is received.

        :param KeepAlivePacket: Keep-alive packet
        :type KeepAlivePacket: PacketKeepAlive
        """
        pass

    def onRequestPacket(self, RequestPacket):
        """Called when a request packet is received.

        :param RequestPacket: Request packet
        :type RequestPacket: PacketRequest
        """
        pass

    def onResultPacket(self, ResultPacket):
        """Called when a result packet is received.

        :param ResultPacket: Result packet
        :type ResultPacket: PacketResult
        """
        pass

    def onMessageEventPacket(self, MessageEventPacket):
        """Called when a message event packet is received.

        :param MessageEventPacket: Message event packet
        :type MessageEventPacket: PacketMessageEvent
        """
        pass

    def onRedirectEventPacket(self, RedirectEventPacket):
        """Called when a redirect event packet is received.

        :param RedirectEventPacket: Redirect event packet
        :type RedirectEventPacket: PacketRedirectEvent
        """
        pass

    def onServerEventPacket(self, ServerEventPacket):
        """Called when a server event packet is received.

        :param ServerEventPacket: Server event packet
        :type ServerEventPacket: PacketServerEvent
        """
        pass

    def _packetDirector(self, packet):
        """Used to redirect the packet to the correct handler.

        :param packet: Received packet
        :type packet: AbstractPacket
        """
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
    """Lilypad client-side protocol implementation which adds handles request responses"""
    sequenceID = 0
    currentRequests = {}

    def onKeepAlivePacket(self, KeepAlivePacket):
        """Called when a keep-alive packet is received.

        When overriding this method, ensure to either call this instance or to handle resending the received
        packet otherwise the client will be disconnected.

        :param KeepAlivePacket: Keep-alive packet
        :type KeepAlivePacket: PacketKeepAlive
        """
        self.writePacket(KeepAlivePacket)

    def writeRequest(self, request):
        """Used to send a request to the connect server. Returns a Deferred that is fired when the
        corresponding result packet is received.

        :param request: Outgoing request
        :type request: AbstractRequest
        :returns :Deferred representing the received result. Callbacks will receive the result
        object, while failbacks will receive a Failure wrapping the status code.
        :rtype :Deferred
        """
        deferred = defer.Deferred()
        packet = PacketRequest(self.sequenceID, request.opcode, requestCodecLookup[request.opcode].encode(request))

        self.currentRequests[self.sequenceID] = (deferred, resultCodecLookup[request.opcode])
        self.sequenceID += 1
        self.writePacket(packet)

        return deferred

    def _packetDirector(self, packet):
        """Overridden _packetDirector to connect the result packet handling.

        :param packet: Received packet
        :type packet: AbstractPacket
        """
        if packet.opcode == 0x02:
            self._resultCallbackHandler(packet)
        super(LilypadProtocol, self)._packetDirector(packet)

    def _resultCallbackHandler(self, resultPacket):
        """Handles connecting the received result with the relevant deferred and codec type.

        :param resultPacket: Received result packet
        :type resultPacket: PacketResult
        """
        if resultPacket.sequenceID not in self.currentRequests:
            raise RuntimeWarning("Could not find deferred for ResultPacket (#" + resultPacket.sequenceID + ")")

        deferred, codec = self.currentRequests.pop(resultPacket.sequenceID)
        if resultPacket.statusCode != StatusCode.SUCCESS:
            deferred.errback(resultPacket.statusCode)
            return
        deferred.callback(codec.decode(resultPacket.payload))


class AutoAuthenticatingLilypadClientProtocol(LilypadClientProtocol):
    """Lilypad client-side protocol implementation which handles authentication with the connect server

    :cvar username: Username to use for authentication with the connect server
    :cvar password: Password to use for authentication with the connect server
    """
    username="example"
    password="example"

    def connectionMade(self):
        salt = self.writeRequest(RequestGetSalt())
        salt.addCallback(self._authenticate)
        salt.addErrback(self._failSalt)

    def _authenticate(self, saltResult):
        result = self.writeRequest(RequestAuthenticate(self.username, saltPassword(self.password, saltResult.salt)))
        result.addCallback(self._passAuth)
        result.addErrback(self._failAuth)

    @staticmethod
    def _failSalt(failCause):
        print "Failed to get salt. Cause was " + StatusCode.pprint(failCause.value)
        return failCause

    @staticmethod
    def _failAuth(failCause):
        print "Failed to authenticate with connect server. Cause was " + StatusCode.pprint(failCause.value)
        return failCause

    @staticmethod
    def _passAuth(authResult):
        print "Successfully authenticated with connect server"