import argparse

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory

from twistedlilypad.LilypadProtocol import AutoAuthenticatingLilypadClientProtocol
from twistedlilypad.Requests.RequestGetSalt import RequestGetSalt
from twistedlilypad.Requests.RequestAuthenticate import RequestAuthenticate
from twistedlilypad.Utilities import saltPassword


class autoAuthenticateLilypadProtocol(AutoAuthenticatingLilypadClientProtocol):
    def connectionMade(self):
        salt = self.writeRequest(RequestGetSalt())
        salt.addCallback(self._authenticate)
        salt.addErrback(self._failSalt)

    def _authenticate(self, saltResult):
        authResult = self.writeRequest(RequestAuthenticate(args.username, saltPassword(args.password, saltResult.salt)))
        authResult.addCallback(self._passAuth)
        authResult.addErrback(self._failAuth)
        if args.auto_close:
            authResult.addCallback(self.scheduleAutoClose)

    def scheduleAutoClose(self, authResult):
        reactor.callLater(15, self.close)

    def close(self, *args, **kwargs):
        self.transport.loseConnection()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', dest='username', default='example')
    parser.add_argument('-p', '--password', dest='password', default='example')
    parser.add_argument('-H', '--host', dest='host', default='localhost')
    parser.add_argument('-P', '--port', dest='port', default=5091, type=int)
    parser.add_argument('-c', '--close', dest='auto_close', action='store_true')

    args = parser.parse_args()

    reactor.connectTCP(args.host, args.port, ReconnectingClientFactory.forProtocol(autoAuthenticateLilypadProtocol))
    reactor.run()