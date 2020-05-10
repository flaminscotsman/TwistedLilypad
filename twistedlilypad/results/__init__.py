from .as_proxy_result import ResultAsProxy, ResultAsProxyCodec
from .as_server_result import ResultAsServer, ResultAsServerCodec
from .authenticate_result import ResultAuthenticate, ResultAuthenticateCodec
from .get_details_result import ResultGetDetails, ResultGetDetailsCodec
from .get_players_result import ResultGetPlayers, ResultGetPlayersCodec
from .get_salt_result import ResultGetSalt, ResultGetSaltCodec
from .get_who_am_i_result import ResultGetWhoAmI, ResultGetWhoAmICodec
from .message_result import ResultMessage, ResultMessageCodec
from .notify_player_result import ResultNotifyPlayer, ResultNotifyPlayerCodec
from .redirect_result import ResultRedirect, ResultRedirectCodec


codecLookup = {
    ResultAsProxy.opcode: ResultAsProxyCodec,
    ResultAsServer.opcode: ResultAsServerCodec,
    ResultAuthenticate.opcode: ResultAuthenticateCodec,
    ResultGetDetails.opcode: ResultGetDetailsCodec,
    ResultGetPlayers.opcode: ResultGetPlayersCodec,
    ResultGetSalt.opcode: ResultGetSaltCodec,
    ResultGetWhoAmI.opcode: ResultGetWhoAmICodec,
    ResultMessage.opcode: ResultMessageCodec,
    ResultNotifyPlayer.opcode: ResultNotifyPlayerCodec,
    ResultRedirect.opcode: ResultRedirectCodec,
}
