from twistedlilypad.Requests.RequestAsProxy import RequestAsProxy, RequestAsProxyCodec
from twistedlilypad.Requests.RequestAsServer import RequestAsServer, RequestAsServerCodec
from twistedlilypad.Requests.RequestAuthenticate import RequestAuthenticate, RequestAuthenticateCodec
from twistedlilypad.Requests.RequestAuthenticate import RequestAuthenticate, RequestAuthenticateCodec
from twistedlilypad.Requests.RequestGetDetails import RequestGetDetails, RequestGetDetailsCodec
from twistedlilypad.Requests.RequestGetPlayers import RequestGetPlayers, RequestGetPlayersCodec
from twistedlilypad.Requests.RequestGetSalt import RequestGetSalt, RequestGetSaltCodec
from twistedlilypad.Requests.RequestGetSalt import RequestGetSalt, RequestGetSaltCodec
from twistedlilypad.Requests.RequestGetWhoAmI import RequestGetWhoAmI, RequestGetWhoAmICodec
from twistedlilypad.Requests.RequestMessage import RequestMessage, RequestMessageCodec
from twistedlilypad.Requests.RequestNotifyPlayer import RequestNotifyPlayer, RequestNotifyPlayerCodec
from twistedlilypad.Requests.RequestRedirect import RequestRedirect, RequestRedirectCodec


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