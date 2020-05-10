import argparse
from functools import partial

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from twistedlilypad.protocol import LilypadClientProtocol
from twistedlilypad.packets.abstract_packet import StatusCode
from twistedlilypad.requests.get_salt_request import RequestGetSalt
from twistedlilypad.requests.authenticate_request import RequestAuthenticate
from twistedlilypad.utilities import salt_password


class filteredMessageLilypadProtocol(LilypadClientProtocol):
    def __init__(self, filter):
        self.filter = filter

    def on_message_event_packet(self, message_event_packet):
        if not self.filter or message_event_packet.channel in self.filter:
            print('{}: {}'.format(message_event_packet.channel, message_event_packet.message))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', dest='username', default='example')
    parser.add_argument('-p', '--password', dest='password', default='example')
    parser.add_argument('-H', '--host', dest='host', default='localhost')
    parser.add_argument('-P', '--port', dest='port', default=5091, type=int)
    parser.add_argument('filter', nargs='*', default=[])

    args = parser.parse_args()

    def failSalt(errcode):
        print("Failed to get salt. Cause was " + StatusCode.pprint(errcode))

    def failAuth(errcode):
        print("Failed to authenticate with connect server. Cause was " + StatusCode.pprint(errcode))

    def passAuth(_):
        print("Successfully authenticated with connect server")

    def authenticate(saltResult, protocol=None):
        authResult = protocol.writeRequest(RequestAuthenticate(args.username, salt_password(args.password, saltResult.salt)))
        authResult.addCallback(passAuth)
        authResult.addErrback(failAuth)

    def getSalt(protocol):
        salt = protocol.writeRequest(RequestGetSalt())
        salt.addCallback(partial(authenticate, protocol=protocol))
        salt.addErrback(failSalt)

    point = TCP4ClientEndpoint(reactor, args.host, args.port)
    d = connectProtocol(point, filteredMessageLilypadProtocol(args.filter))
    d.addCallback(getSalt)

    reactor.run()
