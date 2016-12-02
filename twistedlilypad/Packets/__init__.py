from twistedlilypad.Packets.AbstractPacket import AbstractPacket, AbstractPacketCodec, StatusCode
from twistedlilypad.Packets.PacketKeepAlive import PacketKeepAlive, PacketKeepAliveCodec
from twistedlilypad.Packets.PacketMessageEvent import PacketMessageEvent, PacketMessageEventCodec
from twistedlilypad.Packets.PacketRedirectEvent import PacketRedirectEvent, PacketRedirectEventCodec
from twistedlilypad.Packets.PacketRequest import PacketRequest, PacketRequestCodec
from twistedlilypad.Packets.PacketResult import PacketResult, PacketResultCodec
from twistedlilypad.Packets.PacketServerEvent import PacketServerEvent, PacketServerEventCodec
from twistedlilypad.Packets.PacketPlayerEvent import PacketPlayerEvent, PacketPlayerEventCodec


codecLookup = {
    packet.opcode: packetCodec for packet, packetCodec in (
    (PacketKeepAlive, PacketKeepAliveCodec),
    (PacketMessageEvent, PacketMessageEventCodec),
    (PacketRedirectEvent, PacketRedirectEventCodec),
    (PacketRequest, PacketRequestCodec),
    (PacketResult, PacketResultCodec),
    (PacketServerEvent, PacketServerEventCodec),
    (PacketPlayerEvent, PacketPlayerEventCodec),
)}
""":type : dict[int, AbstractPacketCodec]"""
