import argparse
from functools import partial

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol

from twistedlilypad.LilypadProtocol import LilypadClientProtocol
from twistedlilypad.Packets.AbstractPacket import StatusCode
from twistedlilypad.Requests.RequestGetSalt import RequestGetSalt
from twistedlilypad.Requests.RequestAuthenticate import RequestAuthenticate
from twistedlilypad.Utilities import saltPassword


class filteredMessageLilypadProtocol(LilypadClientProtocol):
    def __init__(self, filter):
        self.filter = filter

    def onMessageEventPacket(self, MessageEventPacket):
        if self.filter and MessageEventPacket in self.filter:
            print '%s: %s' % (MessageEventPacket.channel, MessageEventPacket.message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', dest='username', default='example')
    parser.add_argument('-p', '--password', dest='password', default='example')
    parser.add_argument('-H', '--host', dest='host', default='localhost')
    parser.add_argument('-P', '--port', dest='port', default=5091, type=int)
    parser.add_argument('filter', nargs='*', default=[])

    args = parser.parse_args()

    def failSalt(errcode):
        print "Failed to get salt. Cause was " + StatusCode.pprint(errcode)

    def failAuth(errcode):
        print "Failed to authenticate with connect server. Cause was " + StatusCode.pprint(errcode)

    def passAuth(authResult):
        print "Successfully authenticated with connect server"

    def authenticate(saltResult, protocol=None):
        authResult = protocol.writeRequest(RequestAuthenticate(args.username, saltPassword(args.password, saltResult.salt)))
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