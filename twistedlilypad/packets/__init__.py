from .abstract_packet import AbstractPacket, AbstractPacketCodec, StatusCode
from .keep_alive_packet import PacketKeepAlive, PacketKeepAliveCodec
from .message_event_packet import PacketMessageEvent, PacketMessageEventCodec
from .redirect_event_packet import PacketRedirectEvent, PacketRedirectEventCodec
from .request_packet import PacketRequest, PacketRequestCodec
from .result_packet import PacketResult, PacketResultCodec
from .server_event_packet import PacketServerEvent, PacketServerEventCodec
from .player_event_packet import PacketPlayerEvent, PacketPlayerEventCodec

__all__ = [
    'AbstractPacket', 'StatusCode', 'PacketKeepAlive', 'PacketMessageEvent', 'PacketRedirectEvent', 'PacketRequest',
    'PacketResult', 'PacketServerEvent', 'PacketPlayerEvent', 'codecLookup'
]


codecLookup = {
    PacketKeepAlive.opcode: PacketKeepAliveCodec,
    PacketMessageEvent.opcode: PacketMessageEventCodec,
    PacketRedirectEvent.opcode: PacketRedirectEventCodec,
    PacketRequest.opcode: PacketRequestCodec,
    PacketResult.opcode: PacketResultCodec,
    PacketServerEvent.opcode: PacketServerEventCodec,
    PacketPlayerEvent.opcode: PacketPlayerEventCodec,
}
""":type : dict[int, Type[AbstractPacketCodec]]"""
