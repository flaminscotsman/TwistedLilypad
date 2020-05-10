from twisted.internet import defer
from twisted.internet.protocol import Protocol

from twistedlilypad.packets import *
from twistedlilypad.packets import codecLookup as packetCodecLookup
from twistedlilypad.requests import *
from twistedlilypad.requests import codecLookup as requestCodecLookup
from twistedlilypad.results import codecLookup as resultCodecLookup
from twistedlilypad.utilities import salt_password, varint_parser, varint_parser_with_length, make_packet_stream


class ParserState(object):
    WAITING = 0
    READING_PACKET_OPCODE = 1
    READING_PACKET_PAYLOAD = 2


class LilypadProtocol(Protocol):
    """ Lilypad protocol implementation"""
    _buffer = b''
    _state = ParserState.WAITING

    _payloadSize = 0
    _opcode = 0
    _payload = b''

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
                self._payloadSize, self._buffer = varint_parser(self._buffer)
                self._state = ParserState.READING_PACKET_OPCODE
            except IndexError:
                return  # Just means there wasn't enough data to parse the varint

        if self._state == ParserState.READING_PACKET_OPCODE:
            try:
                self._opcode, self._buffer, opcode_length = varint_parser_with_length(self._buffer)
                self._payloadSize -= opcode_length
                self._state = ParserState.READING_PACKET_PAYLOAD
            except IndexError:
                return  # Just means there wasn't enough data to parse the varint

        if self._state == ParserState.READING_PACKET_PAYLOAD:
            if len(self._buffer) >= self._payloadSize:
                self._payload = self._buffer[:self._payloadSize]
                self._buffer = self._buffer[self._payloadSize:]
                self._state = ParserState.WAITING

                self.raw_packet_received(self._opcode, self._payload)

                packet = packetCodecLookup[self._opcode].decode(self._payload)
                self.packet_received(packet)

                self._packet_director(packet)

    def raw_packet_received(self, opcode, packetData):
        """Called when an unpacked lilypad packet is received.

        :param opcode: Opcode of received packet
        :type opcode: int
        :param packetData: Raw packed data of received packet
        :type opcode: basestring
        """
        pass

    def packet_received(self, packet):
        """Called when a lilypad packet is received.

        :param packet: Parsed lilypad packet
        :type packet: AbstractPacket
        """
        pass

    def write_packet(self, packet):
        """Used to send an outgoing packet.

        :param packet: Outgoing packet
        :type packet: AbstractPacket
        """
        self.transport.write(make_packet_stream(packet))

    def on_keep_alive_packet(self, keep_alive_packet):
        """Called when a keep-alive packet is received.

        :param keep_alive_packet: Keep-alive packet
        :type keep_alive_packet: PacketKeepAlive
        """
        pass

    def on_request_packet(self, request_packet):
        """Called when a request packet is received.

        :param request_packet: Request packet
        :type request_packet: PacketRequest
        """
        pass

    def on_result_packet(self, result_packet):
        """Called when a result packet is received.

        :param result_packet: Result packet
        :type result_packet: PacketResult
        """
        pass

    def on_message_event_packet(self, message_event_packet):
        """Called when a message event packet is received.

        :param message_event_packet: Message event packet
        :type message_event_packet: PacketMessageEvent
        """
        pass

    def on_redirect_event_packet(self, redirect_event_packet):
        """Called when a redirect event packet is received.

        :param redirect_event_packet: Redirect event packet
        :type redirect_event_packet: PacketRedirectEvent
        """
        pass

    def on_server_event_packet(self, server_event_packet):
        """Called when a server event packet is received.

        :param server_event_packet: Server event packet
        :type server_event_packet: PacketServerEvent
        """
        pass

    def on_player_event_packet(self, player_event_packet):
        """Called when a server event packet is received.

        :param player_event_packet: Player event packet
        :type player_event_packet: PacketPlayerEvent
        """
        pass

    def _packet_director(self, packet):
        """Used to redirect the packet to the correct handler.

        :param packet: Received packet
        :type packet: AbstractPacket
        """
        if packet.opcode == 0x00:
            self.on_keep_alive_packet(packet)
        elif packet.opcode == 0x01:
            self.on_request_packet(packet)
        elif packet.opcode == 0x02:
            self.on_result_packet(packet)
        elif packet.opcode == 0x03:
            self.on_message_event_packet(packet)
        elif packet.opcode == 0x04:
            self.on_redirect_event_packet(packet)
        elif packet.opcode == 0x05:
            self.on_server_event_packet(packet)
        elif packet.opcode == 0x06:
            self.on_player_event_packet(packet)
        else:
            raise RuntimeWarning("Unknown packet received")


class LilypadClientProtocol(LilypadProtocol):
    """Lilypad client-side protocol implementation which adds handles request responses"""
    sequenceID = 0
    currentRequests = {}

    def on_keep_alive_packet(self, keep_alive_packet):
        """Called when a keep-alive packet is received.

        When overriding this method, ensure to either call this instance or to handle resending the received
        packet otherwise the client will be disconnected.

        :param keep_alive_packet: Keep-alive packet
        :type keep_alive_packet: PacketKeepAlive
        """
        self.write_packet(keep_alive_packet)

    def writeRequest(self, request):
        """Used to send a request to the connect server. Returns a Deferred that is fired when the
        corresponding result packet is received.

        :param request: Outgoing request
        :type request: abstract_request
        :returns :Deferred representing the received result. Callbacks will receive the result
        object, while failbacks will receive a Failure wrapping the status code.
        :rtype :Deferred
        """
        deferred = defer.Deferred()
        packet = PacketRequest(self.sequenceID, request.opcode, requestCodecLookup[request.opcode].encode(request))

        self.currentRequests[self.sequenceID] = (deferred, resultCodecLookup[request.opcode])
        self.sequenceID += 1
        self.write_packet(packet)

        return deferred

    def _packet_director(self, packet):
        """Overridden _packetDirector to connect the result packet handling.

        :param packet: Received packet
        :type packet: AbstractPacket
        """
        if packet.opcode == 0x02:
            self._result_callback_handler(packet)
        super(LilypadClientProtocol, self)._packet_director(packet)

    def _result_callback_handler(self, result_packet):
        """Handles connecting the received result with the relevant deferred and codec type.

        :param result_packet: Received result packet
        :type result_packet: PacketResult
        """
        request = self.currentRequests.pop(result_packet.sequenceID, None)
        if request is None:
            raise RuntimeWarning("Could not find reference for ResultPacket (#{})".format(result_packet.sequenceID))

        deferred, codec = request
        if result_packet.statusCode != StatusCode.SUCCESS:
            deferred.errback(result_packet.statusCode)
            return
        deferred.callback(codec.decode(result_packet.payload))


class AutoAuthenticatingLilypadClientProtocol(LilypadClientProtocol):
    """Lilypad client-side protocol implementation which handles authentication with the connect server

    :cvar username: Username to use for authentication with the connect server
    :cvar password: Password to use for authentication with the connect server
    """
    username = "example"
    password = "example"

    def connectionMade(self):
        salt = self.writeRequest(RequestGetSalt())
        salt.addCallback(self._authenticate)
        salt.addErrback(self._fail_salt)

    def _authenticate(self, salt_result):
        result = self.writeRequest(RequestAuthenticate(self.username, salt_password(self.password, salt_result.salt)))
        result.addCallback(self._pass_auth)
        result.addErrback(self._fail_auth)

    @staticmethod
    def _fail_salt(cause):
        print("Failed to get salt. Cause was {}".format(StatusCode.pprint(cause.value)))
        return cause

    @staticmethod
    def _fail_auth(cause):
        print("Failed to authenticate with connect server. Cause was " + StatusCode.pprint(cause.value))
        return cause

    @staticmethod
    def _pass_auth(authResult):
        print("Successfully authenticated with connect server")
