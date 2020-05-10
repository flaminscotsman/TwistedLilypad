from unittest import TestCase
from twisted.test import proto_helpers
from twistedlilypad.protocol import LilypadProtocol
from twistedlilypad.packets import *

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock


KEEP_ALIVE_PACKET = PacketKeepAlive(1239812)
KEEP_ALIVE_STRING = b'\x05\x00\x00\x12\xEB\x04'
MESSAGE_EVENT_PACKET = PacketMessageEvent("server", "test", b"Hello World!")
MESSAGE_EVENT_STRING = b'\x1B\x03\x06server\x04test\x00\x0CHello World!'
REDIRECT_EVENT_PACKET = PacketRedirectEvent("server", "player")
REDIRECT_EVENT_STRING = b'\x0F\x04\x06server\x06player'
REQUEST_PACKET = PacketRequest(1, 1, b'\x04user\x04pass')
REQUEST_STRING = b'\x12\x01\x00\x00\x00\x01\x01\x00\x0A\x04user\x04pass'
RESULT_SUCCESS_PACKET = PacketResult(1, StatusCode.SUCCESS, b'\x01\x00')
RESULT_SUCCESS_STRING = b'\x0A\x02\x00\x00\x00\x01\x00\x00\x02\x01\x00'
RESULT_ERROR_PACKET = PacketResult(1, StatusCode.ERROR_GENERIC)
RESULT_ERROR_STRING = b'\x06\x02\x00\x00\x00\x01\x01'
SERVER_EVENT_ADD_PACKET = PacketServerEvent(
    True, 'server', '0123456789abcdef', '127.0.0.1', 25565
)
SERVER_EVENT_ADD_STRING = b'\x26\x05\x01\x06server\x100123456789abcdef\x09127.0.0.1\x63\xDD'
SERVER_EVENT_REMOVE_PACKET = PacketServerEvent(False, 'server')
SERVER_EVENT_REMOVE_STRING = b'\x09\x05\x00\x06server'


class TestLilypadProtocol(TestCase):
    def setUp(self):
        self.transport = proto_helpers.StringTransport()
        self.protocol = LilypadProtocol()
        self.protocol.makeConnection(self.transport)
        
    def test_rawPacketReceived(self):
        callback = Mock()
        self.protocol.raw_packet_received = callback
        self.protocol.dataReceived(KEEP_ALIVE_STRING)
        callback.assert_called_with(0, b'\x00\x12\xEB\x04')

    def test_packetReceived(self):
        callback = Mock()
        self.protocol.packet_received = callback
        self.protocol.dataReceived(KEEP_ALIVE_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(KEEP_ALIVE_PACKET)

    def test_writePacket(self):
        self.protocol.write_packet(KEEP_ALIVE_PACKET)
        self.assertEqual(self.transport.value(), KEEP_ALIVE_STRING)

    def test_onKeepAlivePacket(self):
        callback = Mock()
        self.protocol.on_keep_alive_packet = callback
        self.protocol.dataReceived(KEEP_ALIVE_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(KEEP_ALIVE_PACKET)

    def test_onRequestPacket(self):
        callback = Mock()
        self.protocol.on_request_packet = callback
        self.protocol.dataReceived(REQUEST_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(REQUEST_PACKET)

    def test_onResultPacket(self):
        callback = Mock()
        self.protocol.on_result_packet = callback

        # Check a "success" packet is handled (with payload)
        self.protocol.dataReceived(RESULT_SUCCESS_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(RESULT_SUCCESS_PACKET)

        # Check an "error" packet is handled (without payload)
        callback.reset_mock()
        self.protocol.dataReceived(RESULT_ERROR_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(RESULT_ERROR_PACKET)

    def test_onMessageEventPacket(self):
        callback = Mock()
        self.protocol.on_message_event_packet = callback
        self.protocol.dataReceived(MESSAGE_EVENT_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(MESSAGE_EVENT_PACKET)

    def test_onRedirectEventPacket(self):
        callback = Mock()
        self.protocol.on_redirect_event_packet = callback
        self.protocol.dataReceived(REDIRECT_EVENT_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(REDIRECT_EVENT_PACKET)

    def test_onServerEventPacket(self):
        callback = Mock()
        self.protocol.on_server_event_packet = callback

        # Check a "addition" packet is handled (with addition information)
        self.protocol.dataReceived(SERVER_EVENT_ADD_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(SERVER_EVENT_ADD_PACKET)

        # Check a "removal" packet is handled (without addition information)
        callback.reset_mock()
        self.protocol.dataReceived(SERVER_EVENT_REMOVE_STRING)

        # Check the callback has only been called once and that the received
        #   packet matches what was expected
        callback.assert_called_once_with(SERVER_EVENT_REMOVE_PACKET)
