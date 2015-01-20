from twistedlilypad.Results.ResultAsProxy import ResultAsProxy, ResultAsProxyCodec
from twistedlilypad.Results.ResultAsServer import ResultAsServer, ResultAsServerCodec
from twistedlilypad.Results.ResultAuthenticate import ResultAuthenticate, ResultAuthenticateCodec
from twistedlilypad.Results.ResultGetDetails import ResultGetDetails, ResultGetDetailsCodec
from twistedlilypad.Results.ResultGetPlayers import ResultGetPlayers, ResultGetPlayersCodec
from twistedlilypad.Results.ResultGetSalt import ResultGetSalt, ResultGetSaltCodec
from twistedlilypad.Results.ResultGetWhoAmI import ResultGetWhoAmI, ResultGetWhoAmICodec
from twistedlilypad.Results.ResultMessage import ResultMessage, ResultMessageCodec
from twistedlilypad.Results.ResultNotifyPlayer import ResultNotifyPlayer, ResultNotifyPlayerCodec
from twistedlilypad.Results.ResultRedirect import ResultRedirect, ResultRedirectCodec


codecLookup = {
    result.opcode: resultCodec for result, resultCodec in (
    (ResultAsProxy, ResultAsProxyCodec),
    (ResultAsServer, ResultAsServerCodec),
    (ResultAuthenticate, ResultAuthenticateCodec),
    (ResultGetDetails, ResultGetDetailsCodec),
    (ResultGetPlayers, ResultGetPlayersCodec),
    (ResultGetSalt, ResultGetSaltCodec),
    (ResultGetWhoAmI, ResultGetWhoAmICodec),
    (ResultMessage, ResultMessageCodec),
    (ResultNotifyPlayer, ResultNotifyPlayerCodec),
    (ResultRedirect, ResultRedirectCodec),
)}