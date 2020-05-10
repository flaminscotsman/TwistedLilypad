from twistedlilypad.requests.abstract_request import AbstractRequest
from twistedlilypad.requests.as_proxy_request import RequestAsProxy, RequestAsProxyCodec
from twistedlilypad.requests.as_server_request import RequestAsServer, RequestAsServerCodec
from twistedlilypad.requests.authenticate_request import RequestAuthenticate, RequestAuthenticateCodec
from twistedlilypad.requests.get_details_request import RequestGetDetails, RequestGetDetailsCodec
from twistedlilypad.requests.get_players_request import RequestGetPlayers, RequestGetPlayersCodec
from twistedlilypad.requests.get_salt_request import RequestGetSalt, RequestGetSaltCodec
from twistedlilypad.requests.get_who_am_i_request import RequestGetWhoAmI, RequestGetWhoAmICodec
from twistedlilypad.requests.message_request import RequestMessage, RequestMessageCodec
from twistedlilypad.requests.notify_player_request import RequestNotifyPlayer, RequestNotifyPlayerCodec
from twistedlilypad.requests.redirect_request import RequestRedirect, RequestRedirectCodec


__all__ = [
    'AbstractRequest', 'RequestAsProxy', 'RequestAsServer', 'RequestAuthenticate', 'RequestGetDetails',
    'RequestGetPlayers', 'RequestGetSalt', 'RequestGetWhoAmI', 'RequestMessage', 'RequestNotifyPlayer',
    'RequestRedirect', 'codecLookup'
]

codecLookup = {
    request.opcode: requestCodec for request, requestCodec in (
    (RequestAsProxy, RequestAsProxyCodec),
    (RequestAsServer, RequestAsServerCodec),
    (RequestAuthenticate, RequestAuthenticateCodec),
    (RequestGetDetails, RequestGetDetailsCodec),
    (RequestGetPlayers, RequestGetPlayersCodec),
    (RequestGetSalt, RequestGetSaltCodec),
    (RequestGetWhoAmI, RequestGetWhoAmICodec),
    (RequestMessage, RequestMessageCodec),
    (RequestNotifyPlayer, RequestNotifyPlayerCodec),
    (RequestRedirect, RequestRedirectCodec),
)}
